from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

# Import del db
from db import mongo
from schemas import AcquistoSchema, UpdateAcquistoSchema


# REQUEST ACQUISTO
blp = Blueprint('acquisti', __name__, description='Operazioni sugli acquisti')


@blp.route('/acquisti')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema(many=True))
    # Ottiene tutti gli acquisti
    def get(self):
        acquisto = list(mongo.db.acquisto.find())
        return acquisto


@blp.route('/acquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema)
    # Ottiene i dettagli di un'acquisto specifico
    def get(self, idAcquisto):
        acquisto = mongo.db.acquisto.find_one({"_id": ObjectId(idAcquisto)})
        if not acquisto:
            abort(404, message="Acquisto non trovato")
        return acquisto

@blp.route('/createAcquisti')
class Acquisto(MethodView):
    @blp.arguments(AcquistoSchema)
    @blp.response(201, AcquistoSchema)
    # Crea un nuovo acquisto
    def post(self, dati_acquisto):
        try:
            result = mongo.db.acquisto.insert_one(dati_acquisto)
            acquisto = mongo.db.acquisto.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già un'acquisto con quel nome")
        return acquisto


@blp.route('/updateAcquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.arguments(UpdateAcquistoSchema)
    @blp.response(200, AcquistoSchema)
    # Aggiorna i dettagli di un'acquisto esistente
    def put(self, dati_acquisto, idAcquisto):
        acquisto = mongo.db.acquisto.find_one_and_update(
            {"_id": ObjectId(idAcquisto)},
            {"$set": dati_acquisto},
            return_document=True
        )
        if not acquisto:
            abort(404, message="Acquisto non trovato")
        return acquisto
