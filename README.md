# CalcoloRendimento
Calcolo del rendimento della rete

## Funzionamento
Il programma principale esegue il calcolo del rendimento attraverso la richiesta dei sensori funzionanti nel periodo di interesse e l'estrazione dei dati orari tramite estrattore REM.
Per questo motivo il funzionamento è sotto windows.
Il rendimento è quello definito dalla procedura, ovvero [numero ore funzionamento di tutti i sensori]/ [numero di ore di funzionamento atteso per tutti i sensori]
Il programma contiene una funzione per il calcolo del numero di stazioni con funzionamento di almeno 7500 h/anno (necessario per agorà).


## Requisiti
Il programma funziona sotto macchine windows
Deve essere collegato con il database Meteo
Devono essere installati padas, sqlalchemy e numpy
Deve essere installata in una cartella l'estrattore REM: verificare che la cartella sia correttamente valorizzata

## Note
Il programma non è in versione __user friendly__ pertanto occorre verificarne passo passo il corretto funzionamento.
