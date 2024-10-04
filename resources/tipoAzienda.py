from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId

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
        t_azienda = list(mongo.cx['TopFidelityCard'].tipoAzienda.find())
        return t_azienda


@blp.route('/apiTipiAzienda/tipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema)
    # Ottiene i dettagli di un tipo di azienda specifico
    def get(self, idTipoAzienda):
        try:
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one({"_id": ObjectId(idTipoAzienda)})
            if t_azienda is None:
                abort(404, message="Tipo azienda non trovato")
            return t_azienda
        except InvalidId:
            abort(400, message="Id non valido, riprova")


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(TipoAziendaSchema)
    @blp.response(201, TipoAziendaSchema)
    # Crea un nuovo tipo di azienda
    def post(self, dati_t_azienda):
        try:
            result = mongo.cx['TopFidelityCard'].tipoAzienda.insert_one(dati_t_azienda)
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one({"_id": result.inserted_id})
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            print(field_error)
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        return t_azienda


@blp.route('/apiTipiAzienda/updateTipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, TipoAziendaSchema)
    # Aggiorna i dettagli di un tipo di azienda esistente
    def put(self, dati_t_azienda, idTipoAzienda):
        try:
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one_and_update(
                {"_id": ObjectId(idTipoAzienda)},
                {"$set": dati_t_azienda},
                return_document=True
            )
            if not t_azienda:
                abort(404, message="Tipo azienda non trovato")
            return t_azienda
        except InvalidId:
            abort(400, message="Id tipo azienda non valido, riprova")
