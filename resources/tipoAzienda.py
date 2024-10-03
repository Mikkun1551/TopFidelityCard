from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

# Import del db
from db import mongo
from schemas import TipoAziendaSchema, UpdateTipoAziendaSchema


# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')


@blp.route('/apiTipiAzienda/tipiAzienda')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema(many=True))
    # Ottiene tutti i tipi di azienda
    def get(self):
        tipi_azienda = list(mongo.db.tipoAzienda.find())
        return tipi_azienda


@blp.route('/apiTipiAzienda/tipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema)
    # Ottiene i dettagli di un tipo di azienda specifico
    def get(self, idTipoAzienda):
        t_azienda = mongo.db.tipoAzienda.find_one({"_id": ObjectId(idTipoAzienda)})
        if not t_azienda:
            abort(404, message="Tipo azienda non trovato")
        return t_azienda


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(TipoAziendaSchema)
    @blp.response(201, TipoAziendaSchema)
    # Crea un nuovo tipo di azienda
    def post(self, dati_t_azienda):
        try:
            result = mongo.db.tipoAzienda.insert_one(dati_t_azienda)
            t_azienda = mongo.db.tipoAzienda.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già un tipo azienda con quel nome")
        return t_azienda


@blp.route('/apiTipiAzienda/updateTipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, TipoAziendaSchema)
    # Aggiorna i dettagli di un tipo di azienda esistente
    def put(self, dati_t_azienda, idTipoAzienda):
        t_azienda = mongo.db.tipoAzienda.find_one_and_update(
            {"_id": ObjectId(idTipoAzienda)},
            {"$set": dati_t_azienda},
            return_document=True
        )
        if not t_azienda:
            abort(404, message="Tipo azienda non trovato")
        return t_azienda
