from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

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
        punto_vendita = list(mongo.cx['TopFidelityCard'].puntoVendita.find())
        return punto_vendita


    @blp.arguments(PuntoVenditaSchema)
    @blp.response(201, PuntoVenditaSchema)
    # Crea un nuovo punto vendita
    def post(self, dati_punto_vendita):
        try:
            # Controllo se gli id inseriti nel json della request esistono
            check_azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdAzienda'])})
            if not check_azienda:
                abort(404,
                      message="Azienda inserita inesistenta")
            check_t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdTipoPuntoVendita'])})
            if not check_t_punto_vendita:
                abort(404,
                      message="Tipo punto vendita inserito inesistente")

            result = mongo.cx['TopFidelityCard'].puntoVendita.insert_one(dati_punto_vendita)
            punto_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find_one({"_id": result.inserted_id})
            return punto_vendita
        except TypeError:
            abort(400,
                  message=f"Uno o entrambi gli id inseriti non sono validi, controlla e riprova")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")


@blp.route('/PuntoVendita/<string:idPuntoVendita>')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema)
    # Ottiene i dettagli di un punto vendita specifico
    def get(self, idPuntoVendita):
        try:
            punto_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find_one({"_id": ObjectId(idPuntoVendita)})
            if punto_vendita is None:
                abort(404,
                      message="Punto vendita non trovato")
            return punto_vendita
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")


    @blp.arguments(UpdatePuntoVenditaSchema)
    @blp.response(200, PuntoVenditaSchema)
    # Aggiorna i dettagli di un punto vendita esistente
    def put(self, dati_punto_vendita, idPuntoVendita):
        try:
            # Controllo se gli id inseriti nel json della request esistono
            check_azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdAzienda'])})
            if not check_azienda:
                abort(404,
                      message="Azienda inserita inesistenta")
            check_t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdTipoPuntoVendita'])})
            if not check_t_punto_vendita:
                abort(404,
                      message="Tipo punto vendita inserito inesistente")

            punto_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find_one_and_update(
                {"_id": ObjectId(idPuntoVendita)},
                {"$set": dati_punto_vendita},
                return_document=True
            )
            if not punto_vendita:
                abort(404,
                      message="Punto vendita non trovato")
            return punto_vendita
        except TypeError:
            abort(400,
                  message=f"Uno o entrambi gli id inseriti non sono validi, controlla e riprova")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidDocument:
            abort(400,
                  message="IdAzienda e/o idTipoPuntoVendita "
                          "non valido/i, riprova")
        except InvalidId:
            abort(400,
                  message="Id punto vendita non valido, riprova")
