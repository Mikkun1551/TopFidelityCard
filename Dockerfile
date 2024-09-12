# Immagine base su cui si base l'app
FROM python:3.10
# Non necessario, indica gli autori
LABEL authors="Michel"
# La porta su cui l'api si appoggerà per le requests
EXPOSE 5000
# La cartella di lavoro nel container
WORKDIR /app
# ---
RUN pip install flask
# Selezionare cosa copiare e dove, il . iniziale indica tutto, il secondo
# indica la cartella corrente impostata già su WORKDIR
COPY . .
# Comando da eseguire alla creazione del container, host indica
# l'ip su cui ascoltare, successivamente si indica l'ip address
CMD ["flask", "run", "--host", "0.0.0.0"]
# ENTRYPOINT ["top", "-b"]