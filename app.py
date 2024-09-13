from flask import Flask, request
from flask_smorest import abort
from db import aziende, tipi_azienda, give_id

# Creazione di una flask app
app = Flask(__name__)


# REQUEST AZIENDA
@app.post('/azienda')
def post_azienda():
    # Crea una nuova azienda
    try:
        request_data = request.get_json()
        # Controllo presenza di tutti i parametri nella request
        if (
            'Nome' not in request_data
            or 'Regione' not in request_data
            or 'Città' not in request_data
            or 'idTipoAzienda' not in request_data
        ):
            abort(400, message="Richiesta non valida")
        # Controllo di eventuali duplicati non eliminati rispetto alla request
        for azienda in aziende:
            if (
                request_data['Nome'] == azienda['Nome']
                and request_data['Regione'] == azienda['Regione']
                and request_data['Città'] == azienda['Città']
                and request_data['idTipoAzienda'] == azienda['idTipoAzienda']
                and azienda['eliminato'] == False
            ):
                abort(400, message="Richiesta non valida")
        # Controllo se il tipo azienda inserito esiste
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
        # Se non esiste il tipo azienda inserito abort
        abort(400, message="Richiesta non valida")
    except:
        abort(400, message="Richiesta non valida")


@app.get('/azienda/<int:idAzienda>')
def get_azienda(idAzienda):
    # Ottiene i dettagli di un'azienda specifica
    try:
        for azienda in aziende:
            if (
                azienda['idAzienda'] == idAzienda
                and azienda['eliminato'] == False
            ):
                # Dettagli dell'azienda
                return azienda, 200
        abort(404, message="Azienda non trovata")
    except:
        abort(400, message="Richiesta non valida")


@app.put('/azienda/<int:idAzienda>')
def put_azienda(idAzienda):
    # Aggiorna i dettagli di un'azienda esistente
    try:
        request_data = request.get_json()
        # Controllo presenza di tutti i parametri nella request
        if (
            'Nome' not in request_data
            or 'Regione' not in request_data
            or 'Città' not in request_data
            or 'idTipoAzienda' not in request_data
        ):
            abort(400, message="Richiesta non valida")
        # Controllo se il tipo azienda inserito esiste
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == request_data['idTipoAzienda']:
                # Ricerca azienda nel database
                for azienda in aziende:
                    if (
                        azienda['idAzienda'] == idAzienda
                        and azienda['eliminato'] == False
                    ):
                        azienda['Nome'] = request_data['Nome']
                        azienda['Regione'] = request_data['Regione']
                        azienda['Città'] = request_data['Città']
                        azienda['idTipoAzienda'] = request_data['idTipoAzienda']
                        return {'message': "Dettagli dell'azienda aggiornati con successo"}, 200
        abort(404, message="Azienda non trovata")
    except:
        abort(400, message="Richiesta non valida")


@app.put('/azienda/<int:idAzienda>/delete')
def update_azienda_delete(idAzienda):
    # Elimina logicamente un'azienda impostando il flag "eliminato" su true
    try:
        request_data = request.get_json()
        # Controllo presenza di tutti i parametri nella request
        if (
            'Nome' not in request_data
            or 'Regione' not in request_data
            or 'Città' not in request_data
            or 'idTipoAzienda' not in request_data
        ):
            abort(400, message="Richiesta non valida")
        # Controllo se il tipo azienda inserito esiste
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == request_data['idTipoAzienda']:
                # Ricerca azienda nel database
                for azienda in aziende:
                    if (
                        azienda['idAzienda'] == idAzienda
                        and azienda['eliminato'] == False
                    ):
                        # Flag per indicare se l'azienda è stata eliminata
                        azienda['eliminato'] = True
                        return {'message': "Azienda eliminata logicamente con successo"}, 200
        abort(404, message="Azienda non trovata")
    except:
        abort(400, message="Richiesta non valida")




# REQUEST TIPO AZIENDA
@app.post('/tipo-azienda')
def post_tipo_azienda():
    # Crea un nuovo tipo di azienda
    try:
        request_data = request.get_json()
        # Controllo presenza di tutti i parametri nella request
        if (
            'Nome' not in request_data
            or 'Descrizione' not in request_data
        ):
            abort(400, message="Richiesta non valida")
        # Controllo di eventuali duplicati rispetto alla request
        for t_azienda in tipi_azienda:
            if (
                request_data['Nome'] == t_azienda['Nome']
                and request_data['Descrizione'] == t_azienda['Descrizione']
            ):
                abort(400, message="Richiesta non valida")
        new_tipo_azienda = {
            'idTipoAzienda': give_id('t_azienda'),
            'Nome': request_data['Nome'],
            'Descrizione': request_data['Descrizione']
        }
        tipi_azienda.append(new_tipo_azienda)
        return {'message': "Tipo di azienda creato con successo"}, 201
    except:
        abort(400, message="Richiesta non valida")


@app.get('/tipo-azienda')
def get_tipo_aziende():
    # Ottiene tutti i tipi di azienda
    try:
        # Elenco di tutti i tipi di azienda
        return tipi_azienda, 200
    except:
        abort(400, message="Richiesta non valida")


@app.get('/tipo-azienda/<int:idTipoAzienda>')
def get_tipo_azienda(idTipoAzienda):
    # Ottiene i dettagli di un tipo di azienda specifico
    try:
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == idTipoAzienda:
                # Dettagli del tipo di azienda
                return t_azienda, 200
        abort(404, message="Tipo di azienda non trovato")
    except:
        abort(400, message="Richiesta non valida")


@app.put('/tipo-azienda/<int:idTipoAzienda>')
def put_tipo_azienda(idTipoAzienda):
    # Aggiorna i dettagli di un tipo di azienda esistente
    try:
        request_data = request.get_json()
        # Controllo presenza di tutti i parametri nella request
        if (
            'Nome' not in request_data
            or 'Descrizione' not in request_data
        ):
            abort(400, message="Richiesta non valida")
        # Ricerca tipo azienda nel database
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == idTipoAzienda:
                t_azienda['Nome'] = request_data['Nome']
                t_azienda['Descrizione'] = request_data['Descrizione']
                return {'message': "Dettagli del tipo di azienda aggiornati con successo"}, 200
        abort(404, message="Tipo di azienda non trovato")
    except:
        abort(400, message="Richiesta non valida")


@app.delete('/tipo-azienda/<int:idTipoAzienda>')
def delete_tipo_azienda(idTipoAzienda):
    # Elimina un tipo di azienda
    try:
        for t_azienda in tipi_azienda:
            if t_azienda['idTipoAzienda'] == idTipoAzienda:
                tipi_azienda.remove(t_azienda)
                # Lo status code 204 non restituisce alcun messaggio,
                # nel caso usare uno status code diverso
                return {'message': "Tipo di azienda eliminato con successo"}, 204
        abort(404, message="Tipo di azienda non trovato")
    except:
        abort(400, message="Richiesta non valida")
