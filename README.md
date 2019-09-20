# CalcoloRendimento
Calcolo del rendimento della rete:
1. calcola il numero di stazioni che hanno funzionato per almeno 7200 ore anno. Se il periodo non è un anno lo rapporta a un anno.
2. calcola il numero di ore di funzionamento per il manitentore = Manutenzione e per il parametro B (oppure PP per ETG oppure T per Project Automation)

## Funzionamento
Il programma principale esegue il calcolo del rendimento attraverso la richiesta dei sensori funzionanti nel periodo di interesse e l'estrazione dei dati orari tramite estrattore REM.
Per questo motivo il funzionamento è sotto windows.
Il rendimento è quello definito dalla procedura, ovvero [numero ore funzionamento di tutti i sensori]/ [numero di ore di funzionamento atteso per tutti i sensori]
Il programma contiene una funzione per il calcolo del numero di stazioni con funzionamento di almeno 7200 h/anno (necessario per agorà).


## Requisiti
Il programma funziona sotto macchine windows
Deve essere collegato con il database Meteo
Devono essere installati padas, sqlalchemy e numpy
Deve essere installata in una cartella l'estrattore REM: verificare che la cartella sia correttamente valorizzata

## Note
Il programma non è in versione __user friendly__ pertanto occorre verificarne passo passo il corretto funzionamento.
In particolare:
* occorre inserire manualmente le date di inizio e fine del periodo di interesse
* occorre modificare a mano la Query per selezionare i Sensori
* occorre ricordarsi che se manda il dato di batteria (es. RRQA) bisogna identificare un sensore "diagnostico" (es. T)

# sviluppi
Creazione di un container con estrattore a riga di comando autoconsistente per esecuzione sotto Docker for Windows
1. installare python in windows (la vedo dura) oppure compilare lo script (forse è meglio)
