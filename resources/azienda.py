from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

# Import del db
from db import mongo
from schemas import AziendaSchema, UpdateAziendaSchema


# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')


@blp.route('/apiAzienda/aziende')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema(many=True))
    # Ottiene tutte le azienda
    def get(self):
        azienda = list(mongo.cx['TopFidelityCard'].azienda.find())
        return azienda


@blp.route('/apiAzienda/aziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema)
    # Ottiene i dettagli di un'azienda specifica
    def get(self, idAzienda):
        try:
            azienda = mongo.cx['TopFidelityCard'].azienda.find_one({"_id": ObjectId(idAzienda)})
            if azienda is None:
                abort(404, message="Azienda non trovata")
            return azienda
        except InvalidId:
            abort(400, message="Id non valido, riprova")


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(AziendaSchema)
    @blp.response(201, AziendaSchema)
    # Crea una nuova azienda
    def post(self, dati_azienda):
        #try:
        result = mongo.cx['TopFidelityCard'].azienda.insert_one(dati_azienda)
        azienda = mongo.cx['TopFidelityCard'].azienda.find_one({"_id": result.inserted_id})
        #except DuplicateKeyError:
        #    abort(400, message="Esiste già un'azienda con quel nome")
        return azienda


@blp.route('/apiAzienda/updateAziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    @blp.response(200, AziendaSchema)
    # Aggiorna i dettagli di un'azienda esistente
    def put(self, dati_azienda, idAzienda):
        try:
            azienda = mongo.cx['TopFidelityCard'].azienda.find_one_and_update(
                {"_id": ObjectId(idAzienda)},
                {"$set": dati_azienda},
                return_document=True
            )
            if not azienda:
                abort(404, message="Azienda non trovata")
            return azienda
        except InvalidDocument:
            abort(400,
                  message="IdTipoAzienda non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id azienda non valido, riprova")
