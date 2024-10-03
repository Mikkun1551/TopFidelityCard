from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Import errori mongoDB
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

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
        campagna = list(mongo.db.campagna.find())
        return campagna


@blp.route('/campagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema)
    # Ottiene i dettagli di una campagna specifica
    def get(self, idCampagna):
        campagna = mongo.db.campagna.find_one({"_id": ObjectId(idCampagna)})
        if not campagna:
            abort(404, message="Campagna non trovata")
        return campagna


@blp.route('/createCampagne')
class Campagna(MethodView):
    @blp.arguments(CampagnaSchema)
    @blp.response(201, CampagnaSchema)
    # Crea una nuova campagna
    def post(self, dati_campagna):
        try:
            result = mongo.db.campagna.insert_one(dati_campagna)
            campagna = mongo.db.campagna.find_one({"_id": result.inserted_id})
        except DuplicateKeyError:
            abort(400, message="Esiste già una campagna con quel nome")
        return campagna


@blp.route('/updateCampagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.arguments(UpdateCampagnaSchema)
    @blp.response(200, CampagnaSchema)
    # Aggiorna i dettagli di una campagna esistente
    def put(self, dati_campagna, idCampagna):
        campagna = mongo.db.campagna.find_one_and_update(
            {"_id": ObjectId(idCampagna)},
            {"$set": dati_campagna},
            return_document=True
        )
        if not campagna:
            abort(404, message="Campagna non trovata")
        return campagna
