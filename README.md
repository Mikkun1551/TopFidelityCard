# TopFidelityCard - MongoDB
Il progetto prevede la realizzazione di un applicativo che consenta di gestire i clienti, i loro acquisti e la tessera
a loro associata usando MongoDB come database.

L'applicativo permette di usare tutte le API del documento tecnico, ad eccezione di tutte le DELETE a causa 
della poca chiarezza del documento nel determinare se eseguire una delete normale o una "logica", ossia far sparire l'oggetto
dalle query risultando ancora fisicamente nel database ma mai visualizzabile o interagibile. 
Manca anche la gestione dei token per le operazioni che lo richiedono e l'eventuale scelta di rendere alcuni parametri UNIQUE o no.

Per il database si usa MongoDB e uno schema per mantenere un'integrità dei tipi di dato dei documenti.

E' possibile eseguire l'applicativo tramite container Docker.

Per creare l'immagine:

```docker build -t NOME_IMAGE .```

Per creare il container:

```docker run -p 5000:5000 NOME_IMAGE```

Se vuoi creare un container sincronizzato con la cartella locale (windows):

```docker run -dp 5000:5000 -w /app -v "/c/PATH_ALLA_CARTELLA_DELLA_APP:/app" NOME_IMAGE```
