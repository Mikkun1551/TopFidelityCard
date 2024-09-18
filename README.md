# TopFidelityCard
Il progetto prevede la realizzazione di un applicativo che consenta di gestire i clienti, i loro acquisti e la tessera
a loro associata.

Al momento l'applicativo permette di usare tutte le API del documento tecnico, ad eccezione di tutte le DELETE a causa 
della poca chiarezza del documento riguardo le conseguenze della delete sulle altre tabelle e i vincoli NOT NULL 
su di essi.

Manca anche la gestione dei token per le operazioni che lo richiedono e il settaggio delle unique è stato arbitrario 
visto che nel documento tecnico non si fa riferimento ad esse.

Per il database si usa SQLite in locale in forma persistente, avendo un dockerfile apposito per l'esecuzione 
dell'applicativo, se è necessario svuotare il database basta cancellare il container e crearne un altro. 

Per creare l'immagine:

```docker build -t NOME_IMAGE .```

Per creare il container:

```docker run -p 5005:5000 NOME_IMAGE```

Se vuoi creare un container sincronizzato con la cartella locale (windows):

```docker run -dp 5005:5000 -w /app -v "/c/PATH_ALLA_CARTELLA_DELLA_APP:/app" NOME_IMAGE```
