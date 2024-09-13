from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import aziende, tipi_azienda, give_id


# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')
@blp.route('/azienda')
class Azienda(MethodView):
    def post(self):
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



@blp.route('/azienda/<int:idAzienda>')
class Azienda(MethodView):
    def get(self, idAzienda):
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


    def put(self, idAzienda):
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



@blp.route('/azienda/<int:idAzienda>/delete')
class Azienda(MethodView):
    def put(self, idAzienda):
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
