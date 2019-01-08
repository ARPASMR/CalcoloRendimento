# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 15:58:56 2018

@author: mmussin

Calcolo del rendimento della rete:
    il programma principale calcola il rendimento in percentuale;
    la funzione calcola_rend_PC calcola il numero di stazioni con almeno 7500 h di funzionamento 
    
    ATTENZIONE:
        l'inserimento delle date è manuale
"""
import pandas as pd
import os
import numpy as np
from pandas import Series, DataFrame, Panel
from sqlalchemy import *
import datetime as dt



#preparazione del file di richiesta per l'estrattore
#Query="Select IDsensore,DataFine,DataInizio,Aggregazione from A_Sensori join A_Stazioni on A_Sensori.IDstazione=A_Stazioni.IDstazione where IDrete =1 and NOMEtipologia in ('T','I','Q','N','RN','RG','UR','DV','VV','PP');"
Query="Select IDsensore,A_Sensori.IDstazione,DATE_FORMAT(DataFine,'%Y-%m-%d 00:00:00') as DataFine, DATE_FORMAT(DataInizio,'%Y-%m-%d 00:00:00') as DataInizio,Aggregazione from A_Sensori join A_Stazioni on A_Sensori.IDstazione=A_Stazioni.IDstazione where IDrete in (1,4) and NOMEtipologia in ('T','I','Q','N','RN','RG','UR','DV','VV','PP');"
Query2="Select IDstazione,IDsensore,NOMEtipologia,DataFine,DataInizio,Aggregazione from A_Sensori join A_Stazioni on A_Sensori.IDstazione=A_Stazioni.IDstazione where IDrete in (1,4) and NOMEtipologia in ('T','I','Q','N','RN','RG','UR','DV','VV','PP');"
engine = create_engine('mysql+mysqlconnector://guardone:guardone@10.10.0.6/METEO')
conn=engine.connect()
#df_sensori=pd.read_sql(Query, conn)
df_sensori=pd.read_sql(Query, conn, parse_dates={'DataInizio': '%Y-%m-%d %H:%M:%S','DataFine': '%Y-%m-%d %H:%M:%S'})
# seleziono l'anno che mi interessa
# questo valore va cambiato tutte le volte
anno_r_numero=2018
anno_dopo=anno_r_numero+1
anno_rendimento=dt.date(anno_r_numero,1,1) #mi basta l'anno?
anno_rendimento_fine=dt.date(anno_dopo,1,1)
#anno_rendimento_fine=dt.date(anno_r_numero,12,10) #caso speciale 2017
# print(anno_rendimento_fine.strftime('%Y-%m-%d %H:%M:%S'))
# seleziono tutti gli elementi che hanno la DataFine nulla
df_sensori.DataInizio[df_sensori.DataInizio<anno_rendimento]=anno_rendimento
df_sensori.DataFine[df_sensori.DataFine.isna()]=anno_rendimento_fine
df_sensori.DataFine[df_sensori.DataFine>anno_rendimento_fine]=anno_rendimento_fine
df=df_sensori[df_sensori.DataFine>df_sensori.DataInizio ]
#              &( df_sensori.Aggregazione.isna() || df_sensori.Aggregazione='V')]
df1=df[df.Aggregazione=="V"]
df2=df[df.Aggregazione.isna()]


#devo scrivere su file
#0. cancello il file Richiesta.txt
try:
    os.remove('c:\\users\\mmussin\\desktop\\estrattore rem\\input\\Richiesta.txt')
except:
    print("File di richiesta non esistente")    
#1.creo il nuovo dataframe
df1.insert(loc=0,column='H',value='H')
df1.to_csv('c:\\users\\mmussin\\desktop\\estrattore rem\\input\\Richiesta.txt',sep='\t',columns=['H','IDsensore','DataInizio','DataFine'],header=None,index=False)
df2.insert(loc=0,column='H',value='H')
df2.to_csv('c:\\users\\mmussin\\desktop\\estrattore rem\\input\\Richiesta.txt',sep='\t',columns=['H','IDsensore','DataInizio','DataFine'],header=None,index=False,mode='a')

# esecuzione estrattore
import subprocess
cmd='c:\\users\\mmussin\\desktop\\estrattore rem\\exe\\bin\\estrazionedati.exe'
#os.system('c:\\users\\mmussin\\desktop\\estrattore rem\\exe\\bin\\estrazionedati.exe')
fine=subprocess.run(cmd)
print("Estrazione termitata con codice",fine)



dir_in='c:\\users\\mmussin\\desktop\\Estrattore rem\\output'
#os.remove(dir_in+'Richiesta.end')
lista_files=os.listdir(dir_in)
Cumulatot=0
Cumulaval=0
Cumulav10=0
df_result=pd.DataFrame(columns=['IDsensore','OreTot','OreFunz','OreVal10'])
for f in lista_files:
    print (dir_in+'\\'+f)
    try:
        dffile=pd.read_csv(dir_in+'\\'+f, sep='\t',header=None,names=['IDsensore','DataOra','Misura','Valido'])
    except:
        print("Errore somewhere")
# errore: il 2016 è bisestile!    
#    if(df1.shape[0]>8760):
#        Numvals=df1.shape[0]- 24 #verifico se ci sono 8760 valori
#        
#    else:
    Numvals=dffile.shape[0]-1    
    Validi=dffile[dffile.Valido>=0]
    NV_cod10=dffile[dffile.Valido==-10]
    IDs=dffile.IDsensore[0]
    datafine=df_sensori.DataFine[df_sensori.IDsensore==IDs]
    try:
        data_end=pd.to_datetime(str(datafine.values[0])).strftime("%Y-%m-%d")
    except:
        data_end=anno_rendimento_fine
    datainizio=df_sensori.DataInizio[df_sensori.IDsensore==IDs]
    data_start=pd.to_datetime(str(datainizio.values[0])).strftime("%Y-%m-%d")
    ddelta=(datafine-datainizio)
    hh=ddelta.astype('timedelta64[D]').astype(int).sum()*24
    if(Numvals != hh ):
        print("-->",IDs,hh,Numvals,Validi.shape[0])
    print(f,IDs,Numvals,Validi.shape[0])
    Cumulatot=Numvals+Cumulatot
    Cumulaval=Validi.shape[0]+Cumulaval
    try:
        Cumulav10=NV_cod10.shape[0]+Cumulav10
    except:
        print("tutti i valori sono non validi")
    df_result=df_result.append({'IDsensore':IDs,'OreTot':Numvals,'OreFunz':Validi.shape[0],'OreVal10':NV_cod10.shape[0]},ignore_index=True)
print("Il rendimento complessivo è:",df_result.OreFunz.sum()/df_result.OreTot.sum())
print("considerando anche i dati non validi", (df_result.OreFunz.sum()+df_result.OreVal10.sum())/df_result.OreTot.sum())
#    os.remove(f)
def calcola_rend_PC(data_inizio, data_fine,df):
    """
    data_inizio: dev'essere del tipo 
    data_iniziale=dt.datetime(2018,1,1,0,0,1)
    data_finale=dt.datetime(2018,8,31,23,59,59)
    df è il dataframe dei sensori (in genere df_sensori)
    si presume che ci sia già il campo "SeMin" altrimenti va aggiunto
    """
    ddelta=(data_fine-data_inizio)
    min_funzionamento=ddelta.days*24
    dir_in='c:\\users\\mmussin\\desktop\\Estrattore rem\\output'
    lista_files=os.listdir(dir_in)
    Cumulatot=0
    Cumulaval=0
    Cumulav10=0

    for f in lista_files:
    #print (dir_in+'\\'+f)
        dffile=pd.read_csv(dir_in+'\\'+f, sep='\t',header=None,names=['IDsensore','DataOra','Misura','Valido'])
    # errore: il 2016 è bisestile!    
        if(dffile.shape[0]>min_funzionamento):
            Numvals=dffile.shape[0]- 24 #verifico se ci sono 8760 valori
            df.SeMin[df.IDsensore==dffile.IDsensore[0]]=True
    df.to_csv(path_or_buf='c:\\users\\mmussin\\desktop\\dfsensori.csv')
    grouped=df[df.SeMin==True].groupby('IDstazione')
    print(grouped.sum())
    print(grouped.sum().shape[0])
    