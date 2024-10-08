from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

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
        consumatore = list(mongo.cx['TopFidelityCard'].consumatore.find())
        return consumatore


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema)
    # Ottiene i dettagli di un consumatore specifico
    def get(self, idConsumatore):
        try:
            consumatore = mongo.cx['TopFidelityCard'].consumatore.find_one({"_id": ObjectId(idConsumatore)})
            if consumatore is None:
                abort(404,
                      message="Consumatore non trovato")
            return consumatore
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.arguments(ConsumatoreSchema)
    @blp.response(201, ConsumatoreSchema)
    # Crea un nuovo consumatore
    def post(self, dati_consumatore):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].tessera.find_one({"_id": ObjectId(dati_consumatore['IdTessera'])})
            if not check:
                abort(404,
                      message="Tessera inserita inesistente")

            result = mongo.cx['TopFidelityCard'].consumatore.insert_one(dati_consumatore)
            consumatore = mongo.cx['TopFidelityCard'].consumatore.find_one({"_id": result.inserted_id})
            return consumatore
        except TypeError:
            abort(400,
                  message=f"Id tessera inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            if field_error[0] == 'Nome':
                abort(400,
                      message=f"Richiesta non valida, quell'utente è già associato alla tessera specificata")
            elif field_error[0] == 'Email':
                abort(400,
                      message=f"Richiesta non valida, quella email è già associata alla tessera specificata")
            elif field_error[0] == 'IdTessera':
                abort(400,
                      message=f"Richiesta non valida, può esistere un solo admin per tessera")
            else:
                abort(400,
                      message=f"Richiesta non valida, errore non noto")


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.arguments(UpdateConsumatoreSchema)
    @blp.response(200, ConsumatoreSchema)
    # Aggiorna i dettagli di un consumatore esistente
    def put(self, dati_consumatore, idConsumatore):
        try:
            consumatore = mongo.cx['TopFidelityCard'].consumatore.find_one_and_update(
                {"_id": ObjectId(idConsumatore)},
                {"$set": dati_consumatore},
                return_document=True
            )
            if not consumatore:
                abort(404,
                      message="Consumatore non trovato")
            return consumatore
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            if field_error[0] == 'Nome':
                abort(400,
                      message=f"Richiesta non valida, quell'utente è già associato alla tessera specificata")
            elif field_error[0] == 'Email':
                abort(400,
                      message=f"Richiesta non valida, quella email è già associata alla tessera specificata")
            elif field_error[0] == 'IdTessera':
                abort(400,
                      message=f"Richiesta non valida, può esistere un solo admin per tessera")
            else:
                abort(400,
                      message=f"Richiesta non valida, errore non noto")
        except InvalidDocument:
            abort(400,
                  message="IdTessera non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id consumatore non valido, riprova")
