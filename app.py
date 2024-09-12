from flask import Flask, request

# Creazione di una flask app
app = Flask(__name__)

# PLACEHOLDER DATABASE
aziende = [
    {
        'idAzienda': 1,
        'Nome': 'Apple',
        'Regione': 'Lazio',
        'Città': 'Roma',
        'idTipoAzienda': 1,
        'eliminato': False
    },
    {
        'idAzienda': 2,
        'Nome': 'Sony',
        'Regione': 'Lazio',
        'Città': 'Roma',
        'idTipoAzienda': 1,
        'eliminato': False
    }
]

# PLACEHOLDER REQUEST
@app.get('/azienda')
def get_aziende():
    return {'aziende': aziende}


@app.post('/azienda')
def create_azienda():
    # Crea una nuova azienda
    request_data = request.get_json()
    new_azienda = {
        'idAzienda': request_data['idAzienda'],
        'Nome': request_data['Nome'],
        'Regione': request_data['Regione'],
        'Città': request_data['Città'],
        'idTipoAzienda': request_data['idTipoAzienda'],
        'eliminato': False
    }
    aziende.append(new_azienda)
    return new_azienda, 201


@app.get('/azienda/<int:idAzienda>')
def get_azienda(idAzienda):
    # Ottiene i dettagli di un'azienda specifica
    for azienda in aziende:
        if azienda['idAzienda'] == idAzienda:
            return azienda, 200
    return {'message': 'Azienda non trovata'}, 404
