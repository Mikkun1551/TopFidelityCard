# TopFidelityCard - MongoDB / Docker
Il progetto prevede la realizzazione di una REST API in un container Docker che consente di gestire delle aziende con 
una categoria propria. Da queste aziende si possono gestire delle campagne con premi annessi e dei punti vendita, 
anch'essi con un tipo proprio, a cui fanno rifermimento delle tessere associate a dei consumatori che permettono di 
gestire i loro acquisti.

Per ogni classe del progetto sono previsti 5 metodi: una GET per ricavare tutti gli oggetti di una classe, una GET
per ricavare un oggetto specifico, una POST per creare un oggetto di una classe, una PUT per modificare un oggetto specifico
e una PUT che consiste nell'effettuare una delete logica degli oggetti rendendoli sia invisibili che non interagibili nell'API ma conservandoli
comunque all'interno del database.

Il database utilizzato è MongoDB, per mantenere l'integrità dei dati similmente a un database relazionale si usano degli schema
fatti con la libreria marshmallow e si sfruttano gli indici con vincoli di unicità di MongoDB.

Per creare l'immagine Docker mettersi nella cartella del progetto e digitare il seguente comando:

```docker build -t NOME_IMAGE .```

Per creare il container dall'immagine appena creata:

```docker run -p 5000:5000 NOME_IMAGE```

Se vuoi creare un container sincronizzato con la cartella locale per modificare l'app mantenendola attiva (su windows):

```docker run -dp 5000:5000 -w /app -v "/c/PATH_ALLA_CARTELLA_DELLA_APP:/app" NOME_IMAGE```

Dopo aver avviato il container andare sul seguente link per controllare la documentazione dell'API e le sue request:
http://localhost:5000/swagger-ui
