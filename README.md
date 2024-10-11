# TopFidelityCard - MongoDB / Docker
Il progetto prevede la realizzazione di una REST API in un container docker che consente di gestire delle aziende categorizzate da un tipo proprio.
Da queste aziende si possono gestire delle campagne con premi annessi e dei punti vendita, anch'essi categorizzati
da un tipo proprio, a cui fanno rifermimento delle tessere associate a dei consumatori che permettono di gestire i loro acquisti.

Per ogni classe del progetto sono previsti 5 metodi: una GET per ricavare tutti gli oggetti di una classe, una GET
per ricavare un oggetto specifico di una classe, una POST per creare un oggetto di una classe, una PUT per modificare un oggetto specifico
e una PUT che consiste nell'effettuare una delete logica degli oggetti rendendoli sia invisibili che non interagibili nell'API ma conservandoli
comunque all'interno del database.

Per il database si usa MongoDB e uno schema fatto con marshmallow per mantenere l'integrità dei tipi di dato nei documenti.

Per creare l'immagine Docker trovandosi nella cartella del progetto:

```docker build -t NOME_IMAGE .```

Per creare il container:

```docker run -p 5000:5000 NOME_IMAGE```

Se vuoi creare un container sincronizzato con la cartella locale (windows):

```docker run -dp 5000:5000 -w /app -v "/c/PATH_ALLA_CARTELLA_DELLA_APP:/app" NOME_IMAGE```

Dopo aver avviato il container andare sul seguente link per controllare la documentazione dell'api:
http://localhost:5000/swagger-ui
