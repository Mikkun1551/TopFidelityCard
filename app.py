from flask import Flask, request
from flask_smorest import abort
from db import aziende, tipi_azienda, give_id

# Creazione di una flask app
app = Flask(__name__)


# REQUEST AZIENDA
@app.post('/azienda')
def post_azienda():
    # Crea una nuova azienda
    request_data = request.get_json()
    try:
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == request_data['idTipoAzienda']:
                new_azienda = {
                    'idAzienda': give_id('azienda'),
                    'Nome': request_data['Nome'],
                    'Regione': request_data['Regione'],
                    'Città': request_data['Città'],
                    'idTipoAzienda': request_data['idTipoAzienda'],
                    'eliminato': False
                }
                aziende.append(new_azienda)
                return {'message': "Azienda creata con successo"}, 201
        return {'message': "Richiesta non valida"}, 400
    except:
        return {'message': "Richiesta non valida"}, 400


@app.get('/azienda/<int:idAzienda>')
def get_azienda(idAzienda):
    # Ottiene i dettagli di un'azienda specifica
    for azienda in aziende:
        if azienda['idAzienda'] == idAzienda:
            # Dettagli dell'azienda
            return azienda, 200
    return {'message': 'Azienda non trovata'}, 404



# REQUEST TIPO AZIENDA
@app.post('/tipo-azienda')
def post_tipo_azienda():
    # Crea un nuovo tipo di azienda
    request_data = request.get_json()
    try:
        new_tipo_azienda = {
            'idTipoAzienda': give_id('t_azienda'),
            'Nome': request_data['Nome'],
            'Descrizione': request_data['Descrizione']
        }
        tipi_azienda.append(new_tipo_azienda)
        return {'message': "Tipo di azienda creato con successo"}, 201
    except:
        return {'message': "Richiesta non valida"}, 400


@app.get('/tipo-azienda')
def get_tipo_aziende():
    # Ottiene tutti i tipi di azienda
    # Elenco di tutti i tipi di azienda
    return tipi_azienda, 200
