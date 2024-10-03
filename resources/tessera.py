from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

# Import del db
from db import mongo
from schemas import TesseraSchema, UpdateTesseraSchema


# REQUEST TESSERA
blp = Blueprint('tessere', __name__, description='Operazioni sulle tessere')


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema(many=True))
    # Ottiene tutte le tessere
    def get(self):
        tessera = list(mongo.db.tessera.find())
        return tessera


@blp.route('/tessere_gruppo/<string:idTessera>')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema)
    # Ottiene i dettagli di una tessera specifica
    def get(self, idTessera):
        tessera = mongo.db.tessera.find_one({"_id": ObjectId(idTessera)})
        if not tessera:
            abort(404, message="Tessera non trovata")
        return tessera


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.arguments(TesseraSchema)
    @blp.response(201, TesseraSchema)
    # Crea una nuova tessera
    def post(self, dati_tessera):
        try:
            result = mongo.db.tessera.insert_one(dati_tessera)
            tessera = mongo.db.tessera.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già una tessera con quel nome")
        return tessera


@blp.route('/tessere_gruppo/<string:idTessera>')
class Tessera(MethodView):
    @blp.arguments(UpdateTesseraSchema)
    @blp.response(200, TesseraSchema)
    # Aggiorna i dettagli di una tessera esistente
    def put(self, dati_tessera, idTessera):
        tessera = mongo.db.tessera.find_one_and_update(
            {"_id": ObjectId(idTessera)},
            {"$set": dati_tessera},
            return_document=True
        )
        if not tessera:
            abort(404, message="Tessera non trovata")
        return tessera
