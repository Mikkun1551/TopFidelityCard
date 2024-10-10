from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import AcquistoSchema, UpdateAcquistoSchema, DeleteAcquistoSchema


# REQUEST ACQUISTO
blp = Blueprint('acquisti', __name__, description='Operazioni sugli acquisti')


@blp.route('/acquisti')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema(many=True))
    # Ottiene tutti gli acquisti
    def get(self):
        try:
            acquisto = list(mongo.cx['TopFidelityCard'].acquisto.find({"Eliminato": False}))
            return acquisto
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/acquisti/<string:idAcquisto>')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema)
    # Ottiene i dettagli di un'acquisto specifico
    def get(self, idAcquisto):
        try:
            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one(
                    {"_id": ObjectId(idAcquisto), "Eliminato": False})
            if acquisto is None:
                abort(404,
                      message="Acquisto non trovato")
            return acquisto
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/createAcquisti')
class Acquisto(MethodView):
    @blp.arguments(AcquistoSchema)
    @blp.response(201, AcquistoSchema)
    # Crea un nuovo acquisto
    def post(self, dati_acquisto):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].consumatore.find_one(
                {"_id": ObjectId(dati_acquisto['IdConsumatore']), "Eliminato": False})
            if not check:
                abort(404,
                      message="Consumatore inserito inesistente")

            dati_acquisto['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].acquisto.insert_one(dati_acquisto)
            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one(
                {"_id": result.inserted_id, "Eliminato": False})
            return acquisto
        except TypeError:
            abort(400,
                  message=f"Id consumatore inserito non valido, controlla che sia giusto")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/updateAcquisti/<string:idAcquisto>')
class Acquisto(MethodView):
    @blp.arguments(UpdateAcquistoSchema)
    @blp.response(200, AcquistoSchema)
    # Aggiorna i dettagli di un'acquisto esistente
    def put(self, dati_acquisto, idAcquisto):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].consumatore.find_one(
                {"_id": ObjectId(dati_acquisto['IdConsumatore']), "Eliminato": False})
            if not check:
                abort(404,
                      message="Consumatore inserito inesistente")

            acquisto = mongo.cx['TopFidelityCard'].acquisto.find_one_and_update(
                {"_id": ObjectId(idAcquisto), "Eliminato": False},
                {"$set": dati_acquisto},
                return_document=True)
            if not acquisto:
                abort(404,
                      message="Acquisto non trovato")
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
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/updateAcquisti/delete/<string:idAcquisto>')
class Acquisto(MethodView):
    @blp.arguments(DeleteAcquistoSchema)
    # Cambia il flag eliminato di un'acquisto per cancellarlo logicamente
    def put(self, dati_acquisto, idAcquisto):
        try:
            if dati_acquisto['Eliminato']:
                # Controllo se l'id inserito nella url esiste
                check = mongo.cx['TopFidelityCard'].acquisto.find_one(
                    {"_id": ObjectId(idAcquisto), "Eliminato": False})
                if not check:
                    abort(404,
                          message="Acquisto non trovato")

                # Eliminazione logica
                mongo.cx['TopFidelityCard'].acquisto.update_one(
                    {"_id": ObjectId(idAcquisto), "Eliminato": False},
                    {"$set": {"Eliminato": True}})

                return {'message': "Acquisto eliminato logicamente"}, 200
            else:
                abort(404,
                      message="Impostare il parametro eliminato su true per usare questa procedura")
        except InvalidId:
            abort(400,
                  message="Id acquisto non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
