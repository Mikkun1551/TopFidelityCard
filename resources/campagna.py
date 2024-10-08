from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

# Import del db
from db import mongo
from schemas import CampagnaSchema, UpdateCampagnaSchema


# REQUEST CAMPAGNA
blp = Blueprint('campagne', __name__, description='Operazioni sulle campagne')


@blp.route('/campagne')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema(many=True))
    # Ottiene tutte le campagne
    def get(self):
        campagna = list(mongo.cx['TopFidelityCard'].campagna.find())
        return campagna


@blp.route('/campagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema)
    # Ottiene i dettagli di una campagna specifica
    def get(self, idCampagna):
        try:
            campagna = mongo.cx['TopFidelityCard'].campagna.find_one({"_id": ObjectId(idCampagna)})
            if campagna is None:
                abort(404,
                      message="Campagna non trovata")
            return campagna
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")


@blp.route('/createCampagne')
class Campagna(MethodView):
    @blp.arguments(CampagnaSchema)
    @blp.response(201, CampagnaSchema)
    # Crea una nuova campagna
    def post(self, dati_campagna):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].azienda.find_one({"_id": ObjectId(dati_campagna['IdAzienda'])})
            if not check:
                abort(404,
                      message="Azienda inserita inesistente")

            result = mongo.cx['TopFidelityCard'].campagna.insert_one(dati_campagna)
            campagna = mongo.cx['TopFidelityCard'].campagna.find_one({"_id": result.inserted_id})
            return campagna
        except TypeError:
            abort(400,
                  message=f"Id azienda inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")


@blp.route('/updateCampagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.arguments(UpdateCampagnaSchema)
    @blp.response(200, CampagnaSchema)
    # Aggiorna i dettagli di una campagna esistente
    def put(self, dati_campagna, idCampagna):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].azienda.find_one({"_id": ObjectId(dati_campagna['IdAzienda'])})
            if not check:
                abort(404,
                      message="Azienda inserita inesistente")

            campagna = mongo.cx['TopFidelityCard'].campagna.find_one_and_update(
                {"_id": ObjectId(idCampagna)},
                {"$set": dati_campagna},
                return_document=True
            )
            if not campagna:
                abort(404,
                      message="Campagna non trovata")
            return campagna
        except TypeError:
            abort(400,
                  message=f"Id azienda inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidDocument:
            abort(400,
                  message="IdAzienda non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id campagna non valido, riprova")
