from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

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
        aziende = list(mongo.db.azienda.find())
        return aziende


@blp.route('/apiAzienda/aziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema)
    # Ottiene i dettagli di un'azienda specifica
    def get(self, idAzienda):
        azienda = mongo.db.azienda.find_one({"_id": ObjectId(idAzienda)})
        if not azienda:
            abort(404, message="Azienda non trovata")
        return azienda


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(AziendaSchema)
    @blp.response(201, AziendaSchema)
    # Crea una nuova azienda
    def post(self, dati_azienda):
        try:
            result = mongo.db.azienda.insert_one(dati_azienda)
            azienda = mongo.db.azienda.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già un'a'zienda con quel nome")
        return azienda


@blp.route('/apiAzienda/updateAziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    @blp.response(200, AziendaSchema)
    # Aggiorna i dettagli di un'azienda esistente
    def put(self, dati_azienda, idAzienda):
        azienda = mongo.db.azienda.find_one_and_update(
            {"_id": ObjectId(idAzienda)},
            {"$set": dati_azienda},
            return_document=True
        )
        if not azienda:
            abort(404, message="Azienda non trovata")
        return azienda
