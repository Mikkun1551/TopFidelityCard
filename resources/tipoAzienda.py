from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import tipi_azienda, give_id
from schemas import SchemaTipoAzienda, UpdateTipoAziendaSchema

# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')


@blp.route('/apiTipiAzienda/tipiAzienda')
class TipoAzienda(MethodView):
    @blp.response(200, SchemaTipoAzienda(many=True))
    # Ottiene tutti i tipi di azienda
    def get(self):
        return tipi_azienda.values()


@blp.route('/apiTipiAzienda/tipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, SchemaTipoAzienda)
    # Ottiene i dettagli di un tipo di azienda specifico
    def get(self, idTipoAzienda):
        try:
            return tipi_azienda[idTipoAzienda]
        except KeyError:
            abort(404, message="Tipo azienda non trovato")


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(SchemaTipoAzienda)
    @blp.response(201, SchemaTipoAzienda)
    # Crea un nuovo tipo di azienda
    def post(self, dati_t_azienda):
        # Controllo di eventuali duplicati rispetto alla request
        for t_azienda in tipi_azienda.values():
            if dati_t_azienda['categoria'] == t_azienda['categoria']:
                abort(400, message="Il tipo azienda esiste già")
        id_t_azienda = give_id('t_azienda')
        t_azienda = {**dati_t_azienda, "idTipoAzienda": id_t_azienda}
        tipi_azienda[id_t_azienda] = t_azienda
        return t_azienda


@blp.route('/apiTipiAzienda/updateTipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, SchemaTipoAzienda)
    # Aggiorna i dettagli di un tipo di azienda esistente
    def put(self, dati_t_azienda, idTipoAzienda):
        try:
            t_azienda = tipi_azienda[idTipoAzienda]
            # Aggiornamento del dizionario
            t_azienda |= dati_t_azienda
            return t_azienda
        except KeyError:
            abort(404, message="Tipo azienda non trovato")
