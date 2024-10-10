from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import TesseraSchema, UpdateTesseraSchema, DeleteTesseraSchema


# REQUEST TESSERA
blp = Blueprint('tessere', __name__, description='Operazioni sulle tessere')


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema(many=True))
    # Ottiene tutte le tessere
    def get(self):
        try:
            tessera = list(mongo.cx['TopFidelityCard'].tessera.find({"Eliminato": False}))
            return tessera
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tessere_gruppo/<string:idTessera>')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema)
    # Ottiene i dettagli di una tessera specifica
    def get(self, idTessera):
        try:
            tessera = mongo.cx['TopFidelityCard'].tessera.find_one(
                {"_id": ObjectId(idTessera), "Eliminato": False})
            if not tessera:
                abort(404, message="Tessera non trovata")
            return tessera
        except InvalidId:
            abort(400, message="Id non valido, riprova")
        # Necessario per evitare che if not tessera vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.arguments(TesseraSchema)
    @blp.response(201, TesseraSchema)
    # Crea una nuova tessera
    def post(self, dati_tessera):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].puntoVendita.find_one(
                {"_id": ObjectId(dati_tessera['IdPuntoVendita']), "Eliminato": False})
            if not check:
                abort(404, message="Punto vendita inserito inesistente")

            dati_tessera['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].tessera.insert_one(dati_tessera)
            dati_tessera['_id'] = result.inserted_id
            return dati_tessera
        except TypeError:
            abort(400, message=f"Id punto vendita inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tessere_gruppo/<string:idTessera>')
class Tessera(MethodView):
    @blp.arguments(UpdateTesseraSchema)
    @blp.response(200, TesseraSchema)
    # Aggiorna i dettagli di una tessera esistente
    def put(self, dati_tessera, idTessera):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].puntoVendita.find_one(
                {"_id": ObjectId(dati_tessera['IdPuntoVendita']), "Eliminato": False})
            if not check:
                abort(404, message="Campagna inserita inesistente")

            tessera = mongo.cx['TopFidelityCard'].tessera.find_one_and_update(
                {"_id": ObjectId(idTessera), "Eliminato": False},
                {"$set": dati_tessera},
                return_document=True)
            if not tessera:
                abort(404, message="Tessera non trovata")
            return tessera
        except TypeError:
            abort(400, message=f"Id punto vendita inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidDocument:
            abort(400, message="IdPuntoVendita non valido, riprova")
        except InvalidId:
            abort(400, message="Id tessera non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tessere_gruppo/delete/<string:idTessera>')
class Tessera(MethodView):
    @blp.arguments(DeleteTesseraSchema)
    # Cambia il flag eliminato di una tessera per cancellarla logicamente
    def put(self, dati_tessera, idTessera):
        try:
            # Controllo che la procedura venga avviata
            if not dati_tessera['Eliminato']:
                abort(404, message="Impostare il parametro eliminato su true per usare questa procedura")

            # Controllo se l'id inserito nella url esiste
            check = mongo.cx['TopFidelityCard'].tessera.find_one(
                {"_id": ObjectId(idTessera), "Eliminato": False})
            if not check:
                abort(404, message="Tessera non trovata")

            # Eliminazione logica tessera
            mongo.cx['TopFidelityCard'].tessera.update_one(
                {"_id": ObjectId(idTessera), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            # Controllo dei consumatori legati alla tessera eliminata
            consumatori = mongo.cx['TopFidelityCard'].consumatore.find(
                {"IdTessera": ObjectId(idTessera), "Eliminato": False})

            # Eliminazione degli acquisti legati ai consumatori eliminati
            for consumatore in consumatori:
                mongo.cx['TopFidelityCard'].acquisto.update_many(
                    {"IdConsumatore": consumatore['_id'], "Eliminato": False},
                    {"$set": {"Eliminato": True}})

            # Eliminazione logica su consumatore
            mongo.cx['TopFidelityCard'].consumatore.update_many(
                {"IdTessera": ObjectId(idTessera), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            return {'message': "Tessera e relativi documenti eliminati logicamente"}, 200

        except InvalidId:
            abort(400, message="Id tessera non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
