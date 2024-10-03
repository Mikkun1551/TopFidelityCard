from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

# Import del db
from db import mongo
from schemas import ConsumatoreSchema, UpdateConsumatoreSchema


# REQUEST CONSUMATORE
blp = Blueprint('consumatori', __name__, description='Operazioni sui consumatori')


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema(many=True))
    # Ottiene tutti i consumatori
    def get(self):
        consumatore = list(mongo.db.consumatore.find())
        return consumatore


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema)
    # Ottiene i dettagli di un consumatore specifico
    def get(self, idConsumatore):
        consumatore = mongo.db.consumatore.find_one({"_id": ObjectId(idConsumatore)})
        if not consumatore:
            abort(404, message="Consumatore non trovato")
        return consumatore


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.arguments(ConsumatoreSchema)
    @blp.response(201, ConsumatoreSchema)
    # Crea un nuovo consumatore
    def post(self, dati_consumatore):
        try:
            result = mongo.db.consumatore.insert_one(dati_consumatore)
            consumatore = mongo.db.consumatore.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già un consumatore con quel nome")
        return consumatore


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.arguments(UpdateConsumatoreSchema)
    @blp.response(200, ConsumatoreSchema)
    # Aggiorna i dettagli di un consumatore esistente
    def put(self, dati_consumatore, idConsumatore):
        consumatore = mongo.db.consumatore.find_one_and_update(
            {"_id": ObjectId(idConsumatore)},
            {"$set": dati_consumatore},
            return_document=True
        )
        if not consumatore:
            abort(404, message="Consumatore non trovato")
        return consumatore
