from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

# Import del db
from db import mongo
from schemas import PuntoVenditaSchema, UpdatePuntoVenditaSchema


# REQUEST PUNTO VENDITA
blp = Blueprint('puntiVendita', __name__, description='Operazioni sui punti vendita')


@blp.route('/PuntoVendita')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema(many=True))
    # Ottiene tutti i punti vendita
    def get(self):
        punto_vendita = list(mongo.db.puntoVendita.find())
        return punto_vendita


    @blp.arguments(PuntoVenditaSchema)
    @blp.response(201, PuntoVenditaSchema)
    # Crea un nuovo punto vendita
    def post(self, dati_punto_vendita):
        try:
            result = mongo.db.puntoVendita.insert_one(dati_punto_vendita)
            punto_vendita = mongo.db.puntoVendita.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già un punto vendita con quel nome")
        return punto_vendita


@blp.route('/PuntoVendita/<string:idPuntoVendita>')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema)
    # Ottiene i dettagli di un punto vendita specifico
    def get(self, idPuntoVendita):
        punto_vendita = mongo.db.puntoVendita.find_one({"_id": ObjectId(idPuntoVendita)})
        if not punto_vendita:
            abort(404, message="Punto vendita non trovato")
        return punto_vendita


    @blp.arguments(UpdatePuntoVenditaSchema)
    @blp.response(200, PuntoVenditaSchema)
    # Aggiorna i dettagli di un punto vendita esistente
    def put(self, dati_punto_vendita, idPuntoVendita):
        punto_vendita = mongo.db.puntoVendita.find_one_and_update(
            {"_id": ObjectId(idPuntoVendita)},
            {"$set": dati_punto_vendita},
            return_document=True
        )
        if not punto_vendita:
            abort(404, message="Punto vendita non trovato")
        return punto_vendita
