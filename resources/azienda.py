from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import give_id
from schemas import AziendaSchema, UpdateAziendaSchema

# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')


@blp.route('/apiAzienda/aziende')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema(many=True))
    # Ottiene tutte le azienda
    def get(self):
        return aziende.values()


@blp.route('/apiAzienda/aziende/<int:idAzienda>')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema)
    # Ottiene i dettagli di un'azienda specifica
    def get(self, idAzienda):
        try:
            return aziende[idAzienda]
        except KeyError:
            abort(404, message="Azienda non trovata")


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(AziendaSchema)
    @blp.response(201, AziendaSchema)
    # Crea una nuova azienda
    def post(self, dati_azienda):
        # Controllo di eventuali duplicati rispetto alla request
        for azienda in aziende.values():
            if (
                dati_azienda['nome'] == azienda['nome']
                and dati_azienda['regione'] == azienda['regione']
                and dati_azienda['citta'] == azienda['citta']
                and dati_azienda['cap'] == azienda['cap']
                and dati_azienda['piva'] == azienda['piva']
                and dati_azienda['idTipoAzienda'] == azienda['idTipoAzienda']
            ):
                abort(400, message="L'azienda esiste già")
        # Controllo se il tipo azienda inserito esiste
        for t_azienda in tipi_azienda.values():
            if t_azienda['idTipoAzienda'] == dati_azienda['idTipoAzienda']:
                id_azienda = give_id('azienda')
                azienda = {**dati_azienda, "idAzienda": id_azienda}
                aziende[id_azienda] = azienda
                return azienda
        # Se non esiste il tipo azienda inserito abort
        abort(400, message="Richiesta non valida, tipo azienda inesistente")


@blp.route('/apiAzienda/updateAziende/<int:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    @blp.response(200, AziendaSchema)
    # Aggiorna i dettagli di un'azienda esistente
    def put(self, dati_azienda, idAzienda):
        try:
            azienda = aziende[idAzienda]
            # Aggiornamento del dizionario
            azienda |= dati_azienda
            return azienda
        except KeyError:
            abort(404, message="Azienda non trovata")
