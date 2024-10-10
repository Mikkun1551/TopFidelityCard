from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import ConsumatoreSchema, UpdateConsumatoreSchema, DeleteConsumatoreSchema


# REQUEST CONSUMATORE
blp = Blueprint('consumatori', __name__, description='Operazioni sui consumatori')


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema(many=True))
    # Ottiene tutti i consumatori
    def get(self):
        try:
            consumatore = list(mongo.cx['TopFidelityCard'].consumatore.find({"Eliminato": False}))
            return consumatore
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema)
    # Ottiene i dettagli di un consumatore specifico
    def get(self, idConsumatore):
        try:
            consumatore = mongo.cx['TopFidelityCard'].consumatore.find_one(
                {"_id": ObjectId(idConsumatore), "Eliminato": False})
            if not consumatore:
                abort(404,
                      message="Consumatore non trovato")
            return consumatore
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")
        # Necessario per evitare che if not consumatore vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.arguments(ConsumatoreSchema)
    @blp.response(201, ConsumatoreSchema)
    # Crea un nuovo consumatore
    def post(self, dati_consumatore):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].tessera.find_one(
                {"_id": ObjectId(dati_consumatore['IdTessera']), "Eliminato": False})
            if not check:
                abort(404,
                      message="Tessera inserita inesistente")

            dati_consumatore['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].consumatore.insert_one(dati_consumatore)
            dati_consumatore['_id'] = result.inserted_id
            return dati_consumatore
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
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.arguments(UpdateConsumatoreSchema)
    @blp.response(200, ConsumatoreSchema)
    # Aggiorna i dettagli di un consumatore esistente
    def put(self, dati_consumatore, idConsumatore):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].tessera.find_one(
                {"_id": ObjectId(dati_consumatore['IdTessera']), "Eliminato": False})
            if not check:
                abort(404,
                      message="Tessera inserita inesistente")

            consumatore = mongo.cx['TopFidelityCard'].consumatore.find_one_and_update(
                {"_id": ObjectId(idConsumatore), "Eliminato": False},
                {"$set": dati_consumatore},
                return_document=True)
            if not consumatore:
                abort(404,
                      message="Consumatore non trovato")
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
        except InvalidDocument:
            abort(400,
                  message="IdTessera non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id consumatore non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/consumatori/delete/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.arguments(DeleteConsumatoreSchema)
    # Cambia il flag eliminato di un consumatore per cancellarlo logicamente
    def put(self, dati_consumatore, idConsumatore):
        try:
            # Controllo che la procedura venga avviata
            if not dati_consumatore['Eliminato']:
                abort(404, message="Impostare il parametro eliminato su true per usare questa procedura")

            # Controllo se l'id inserito nella url esiste
            check = mongo.cx['TopFidelityCard'].consumatore.find_one(
                {"_id": ObjectId(idConsumatore), "Eliminato": False})
            if not check:
                abort(404,
                      message="Consumatore non trovato")

            # Eliminazione logica consumatore
            mongo.cx['TopFidelityCard'].consumatore.update_one(
                {"_id": ObjectId(idConsumatore), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            # Eliminazione logica su acquisto
            mongo.cx['TopFidelityCard'].acquisto.update_many(
                {"IdConsumatore": ObjectId(idConsumatore), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            return {'message': "Consumatore e relativi acquisti eliminati logicamente"}, 200

        except InvalidId:
            abort(400,
                  message="Id consumatore non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
