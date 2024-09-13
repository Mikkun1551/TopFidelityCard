from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import tipi_azienda, give_id


# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')
@blp.route('/tipo-azienda')
class TipoAzienda(MethodView):
    def post(self):
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


    def get(self):
        # Ottiene tutti i tipi di azienda
        try:
            # Elenco di tutti i tipi di azienda
            return tipi_azienda, 200
        except:
            abort(400, message="Richiesta non valida")



@blp.route('/tipo-azienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    def get(self, idTipoAzienda):
        # Ottiene i dettagli di un tipo di azienda specifico
        try:
            for t_azienda in tipi_azienda:
                if t_azienda['idTipoAzienda'] == idTipoAzienda:
                    # Dettagli del tipo di azienda
                    return t_azienda, 200
            abort(404, message="Tipo di azienda non trovato")
        except:
            abort(400, message="Richiesta non valida")


    def put(self, idTipoAzienda):
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


    def delete(self, idTipoAzienda):
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
