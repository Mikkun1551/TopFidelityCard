from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import tipi_azienda, give_id
from schemas import SchemaTipoAzienda, UpdateTipoAziendaSchema

# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')
@blp.route('/apiTipiAzienda/tipiAzienda')
class TipoAzienda(MethodView):
    @blp.response(200, SchemaTipoAzienda(many=True))
    def get(self):
        # Ottiene tutti i tipi di azienda
        try:
            # Elenco di tutti i tipi di azienda
            return tipi_azienda
        except:
            abort(400, message="Richiesta non valida")


@blp.route('/apiTipiAzienda/tipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, SchemaTipoAzienda)
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


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(SchemaTipoAzienda)
    @blp.response(201, SchemaTipoAzienda)
    def post(self, dati_t_azienda):
        # Crea un nuovo tipo di azienda
        try:
            # Controllo di eventuali duplicati rispetto alla request
            for t_azienda in tipi_azienda:
                if (
                    dati_t_azienda['Categoria'] == t_azienda['Categoria']
                    and dati_t_azienda['Descrizione'] == t_azienda['Descrizione']
                ):
                    abort(400, message="Richiesta non valida")
            new_tipo_azienda = {
                'idTipoAzienda': give_id('t_azienda'),
                'Categoria': dati_t_azienda['Categoria'],
                'Descrizione': dati_t_azienda['Descrizione']
            }
            tipi_azienda.append(new_tipo_azienda)
            return {'message': "Tipo di azienda creato con successo"}
        except:
            abort(400, message="Richiesta non valida")


@blp.route('/apiTipiAzienda/updateTipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, SchemaTipoAzienda)
    def put(self, dati_t_azienda, idTipoAzienda):
        # Aggiorna i dettagli di un tipo di azienda esistente
        try:
            # Ricerca tipo azienda nel database
            for t_azienda in tipi_azienda:
                if t_azienda['idTipoAzienda'] == idTipoAzienda:
                    t_azienda['Categoria'] = dati_t_azienda['Categoria']
                    t_azienda['Descrizione'] = dati_t_azienda['Descrizione']
                    return {'message': "Dettagli del tipo di azienda aggiornati con successo"}
            abort(404, message="Tipo di azienda non trovato")
        except:
            abort(400, message="Richiesta non valida")
