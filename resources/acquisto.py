from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

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
        acquisto = list(mongo.cx['TopFidelityCard'].acquisto.find())
        return acquisto


@blp.route('/acquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema)
    # Ottiene i dettagli di un'acquisto specifico
    def get(self, idAcquisto):
        try:
            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one({"_id": ObjectId(idAcquisto)})
            if acquisto is None:
                abort(404, message="Acquisto non trovato")
            return acquisto
        except InvalidId:
            abort(400, message="Id non valido, riprova")


@blp.route('/createAcquisti')
class Acquisto(MethodView):
    @blp.arguments(AcquistoSchema)
    @blp.response(201, AcquistoSchema)
    # Crea un nuovo acquisto
    def post(self, dati_acquisto):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].consumatore.find_one({"_id": ObjectId(dati_acquisto['IdConsumatore'])})
            if not check:
                abort(404,
                      message="Consumatore inserito inesistente")

            result = mongo.cx['TopFidelityCard'].acquisto.insert_one(dati_acquisto)
            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one({"_id": result.inserted_id})
            return acquisto
        except TypeError:
            abort(400,
                  message=f"Id consumatore inserito non valido, controlla che sia giusto")


@blp.route('/updateAcquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.arguments(UpdateAcquistoSchema)
    @blp.response(200, AcquistoSchema)
    # Aggiorna i dettagli di un'acquisto esistente
    def put(self, dati_acquisto, idAcquisto):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].consumatore.find_one({"_id": ObjectId(dati_acquisto['IdConsumatore'])})
            if not check:
                abort(404,
                      message="Consumatore inserito inesistente")

            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one_and_update(
                {"_id": ObjectId(idAcquisto)},
                {"$set": dati_acquisto},
                return_document=True
            )
            if not acquisto:
                abort(404, message="Acquisto non trovato")
            return acquisto
        except TypeError:
            abort(400,
                  message=f"Id consumatore inserito non valido, controlla che sia giusto")
        except InvalidDocument:
            abort(400,
                  message="IdConsumatore non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id acquisto non valido, riprova")
