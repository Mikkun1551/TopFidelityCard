from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import aziende, tipi_azienda, give_id
from schemas import SchemaAzienda, UpdateAziendaSchema

# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')
@blp.route('/apiAzienda/aziende')
class Azienda(MethodView):
    def get(self):
        # Ottiene tutte le azienda
        try:
            # Elenco di tutte le aziende
            return aziende, 200
        except:
            abort(400, message="Richiesta non valida")


@blp.route('/apiAzienda/aziende/<int:idAzienda>')
class Azienda(MethodView):
    def get(self, idAzienda):
        # Ottiene i dettagli di un'azienda specifica
        try:
            for azienda in aziende:
                if azienda['idAzienda'] == idAzienda:
                    # Dettagli dell'azienda
                    return azienda, 200
            abort(404, message="Azienda non trovata")
        except:
            abort(400, message="Richiesta non valida")


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(SchemaAzienda)
    def post(self, dati_azienda):
        # Crea una nuova azienda
        try:
            # Controllo di eventuali duplicati rispetto alla request
            for azienda in aziende:
                if (
                    dati_azienda['Nome'] == azienda['Nome']
                    and dati_azienda['Regione'] == azienda['Regione']
                    and dati_azienda['Città'] == azienda['Città']
                    and dati_azienda['Cap'] == azienda['Cap']
                    and dati_azienda['PartitaIva'] == azienda['PartitaIva']
                    and dati_azienda['idTipoAzienda'] == azienda['idTipoAzienda']

                ):
                    abort(400, message="Richiesta non valida")
            # Controllo se il tipo azienda inserito esiste
            for t_azienda in tipi_azienda:
                if t_azienda['idTipoAzienda'] == dati_azienda['idTipoAzienda']:
                    new_azienda = {
                        'idAzienda': give_id('azienda'),
                        'Nome': dati_azienda['Nome'],
                        'Regione': dati_azienda['Regione'],
                        'Città': dati_azienda['Città'],
                        'Cap': dati_azienda['Cap'],
                        'PartitaIva': dati_azienda['PartitaIva'],
                        'idTipoAzienda': dati_azienda['idTipoAzienda'],
                    }
                    aziende.append(new_azienda)
                    return {'message': "Azienda creata con successo"}, 201
            # Se non esiste il tipo azienda inserito abort
            abort(400, message="Richiesta non valida")
        except:
            abort(400, message="Richiesta non valida")


@blp.route('/apiAzienda/updateAziende/<int:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    def put(self, dati_azienda, idAzienda):
        # Aggiorna i dettagli di un'azienda esistente
        try:
            # Controllo se il tipo azienda inserito esiste
            for t_azienda in tipi_azienda:
                if t_azienda['idTipoAzienda'] == dati_azienda['idTipoAzienda']:
                    # Ricerca azienda nel database
                    for azienda in aziende:
                        if azienda['idAzienda'] == idAzienda:
                            azienda['Nome'] = dati_azienda['Nome']
                            azienda['Regione'] = dati_azienda['Regione']
                            azienda['Città'] = dati_azienda['Città']
                            azienda['Cap'] = dati_azienda['Cap']
                            azienda['PartitaIva'] = dati_azienda['PartitaIva']
                            azienda['idTipoAzienda'] = dati_azienda['idTipoAzienda']
                            return {'message': "Dettagli dell'azienda aggiornati con successo"}, 200
            abort(404, message="Azienda non trovata")
        except:
            abort(400, message="Richiesta non valida")
