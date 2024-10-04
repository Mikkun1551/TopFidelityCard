from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

# Import del db
from db import mongo
from schemas import PremioSchema, UpdatePremioSchema


# REQUEST PREMIO
blp = Blueprint('premi', __name__, description='Operazioni sui premi')


@blp.route('/premi')
class Premio(MethodView):
    @blp.response(200, PremioSchema(many=True))
    # Ottiene tutti i premi
    def get(self):
        premio = list(mongo.cx['TopFidelityCard'].premio.find())
        return premio


@blp.route('/premi/<string:idPremio>')
class Premio(MethodView):
    @blp.response(200, PremioSchema)
    # Ottiene i dettagli di un premio specifico
    def get(self, idPremio):
        try:
            premio = mongo.cx['TopFidelityCard'].premio.find_one({"_id": ObjectId(idPremio)})
            if premio is None:
                abort(404, message="Premio non trovato")
            return premio
        except InvalidId:
            abort(400, message="Premio non trovato")


@blp.route('/createPremi')
class Premio(MethodView):
    @blp.arguments(PremioSchema)
    @blp.response(201, PremioSchema)
    # Crea un nuovo premio
    def post(self, dati_premio):
        #try:
        result = mongo.cx['TopFidelityCard'].premio.insert_one(dati_premio)
        premio = mongo.cx['TopFidelityCard'].premio.find_one({"_id": result.inserted_id})
        #except DuplicateKeyError:
        #    abort(400, message="Esiste già un premio con quel nome")
        return premio


@blp.route('/updatePremi/<string:idPremio>')
class Premio(MethodView):
    @blp.arguments(UpdatePremioSchema)
    @blp.response(200, PremioSchema)
    # Aggiorna i dettagli di un premio esistente
    def put(self, dati_premio, idPremio):
        try:
            premio = mongo.cx['TopFidelityCard'].premio.find_one_and_update(
                {"_id": ObjectId(idPremio)},
                {"$set": dati_premio},
                return_document=True
            )
            if not premio:
                abort(404, message="Premio non trovato")
            return premio
        except InvalidDocument:
            abort(400,
                  message="IdCampagna non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id premio non valido, riprova")
