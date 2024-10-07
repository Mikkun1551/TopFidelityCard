from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId

# Import del db
from db import mongo
from schemas import TipoPuntoVenditaSchema, UpdateTipoPuntoVenditaSchema


# REQUEST TIPO PUNTO VENDITA
blp = Blueprint('tipiPuntoVendita', __name__, description='Operazioni sui tipi punto vendita')


@blp.route('/tipoPuntoVendita')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema(many=True))
    # Ottiene tutti i tipi di punto vendita
    def get(self):
        t_punto_vendita = list(mongo.cx['TopFidelityCard'].tipoPuntoVendita.find())
        return t_punto_vendita


    @blp.arguments(TipoPuntoVenditaSchema)
    @blp.response(201, TipoPuntoVenditaSchema)
    # Crea un nuovo tipo di punto vendita
    def post(self, dati_t_punto_vendita):
        try:
            result = mongo.cx['TopFidelityCard'].tipoPuntoVendita.insert_one(dati_t_punto_vendita)
            t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one({"_id": result.inserted_id})
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        return t_punto_vendita


@blp.route('/tipoPuntoVendita/<string:idTipoPuntoVendita>')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema)
    # Ottiene i dettagli di un tipo punto vendita specifico
    def get(self, idTipoPuntoVendita):
        try:
            t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one({"_id": ObjectId(idTipoPuntoVendita)})
            if t_punto_vendita is None:
                abort(404, message="Tipo punto vendita non trovato")
            return t_punto_vendita
        except InvalidId:
            abort(400, message="Id non valido, riprova")


    @blp.arguments(UpdateTipoPuntoVenditaSchema)
    @blp.response(200, TipoPuntoVenditaSchema)
    # Aggiorna i dettagli di un tipo punto vendita esistente
    def put(self, dati_t_punto_vendita, idTipoPuntoVendita):
        try:
            t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one_and_update(
                {"_id": ObjectId(idTipoPuntoVendita)},
                {"$set": dati_t_punto_vendita},
                return_document=True
            )
            if not t_punto_vendita:
                abort(404, message="Tipo punto vendita non trovato")
            return t_punto_vendita
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidId:
            abort(400, message="Id non valido, riprova")
