from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import TipoPuntoVenditaSchema, UpdateTipoPuntoVenditaSchema, DeleteTipoPuntoVenditaSchema


# REQUEST TIPO PUNTO VENDITA
blp = Blueprint('tipiPuntoVendita', __name__, description='Operazioni sui tipi punto vendita')


@blp.route('/tipoPuntoVendita')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema(many=True))
    # Ottiene tutti i tipi di punto vendita
    def get(self):
        try:
            t_punto_vendita = list(mongo.cx['TopFidelityCard'].tipoPuntoVendita.find({"Eliminato": False}))
            return t_punto_vendita
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


    @blp.arguments(TipoPuntoVenditaSchema)
    @blp.response(201, TipoPuntoVenditaSchema)
    # Crea un nuovo tipo di punto vendita
    def post(self, dati_t_punto_vendita):
        try:
            dati_t_punto_vendita['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].tipoPuntoVendita.insert_one(dati_t_punto_vendita)
            dati_t_punto_vendita['_id'] = result.inserted_id
            return dati_t_punto_vendita
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tipoPuntoVendita/<string:idTipoPuntoVendita>')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema)
    # Ottiene i dettagli di un tipo punto vendita specifico
    def get(self, idTipoPuntoVendita):
        try:
            t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(idTipoPuntoVendita), "Eliminato": False})
            if not t_punto_vendita:
                abort(404, message="Tipo punto vendita non trovato")
            return t_punto_vendita
        except InvalidId:
            abort(400, message="Id inserito non valido, riprova")
        # Necessario per evitare che if not t_punto_vendita vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


    @blp.arguments(UpdateTipoPuntoVenditaSchema)
    @blp.response(200, TipoPuntoVenditaSchema)
    # Aggiorna i dettagli di un tipo punto vendita esistente
    def put(self, dati_t_punto_vendita, idTipoPuntoVendita):
        try:
            t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one_and_update(
                {"_id": ObjectId(idTipoPuntoVendita), "Eliminato": False},
                {"$set": dati_t_punto_vendita},
                return_document=True)
            if not t_punto_vendita:
                abort(404, message="Tipo punto vendita non trovato")
            return t_punto_vendita
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidId:
            abort(400, message="Id tipo punto vendita non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/tipoPuntoVendita/delete/<string:idTipoPuntoVendita>')
class TipoPuntoVendita(MethodView):
    @blp.arguments(DeleteTipoPuntoVenditaSchema)
    # Cambia il flag eliminato di un tipo punto vendita per cancellarlo logicamente
    def put(self, dati_t_punto_vendita, idTipoPuntoVendita):
        try:
            # Controllo che la procedura venga avviata
            if not dati_t_punto_vendita['Eliminato']:
                abort(404, message="Impostare il parametro eliminato su true per usare questa procedura")

            # Controllo se l'id inserito nella url esiste
            check = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(idTipoPuntoVendita), "Eliminato": False})
            if not check:
                abort(404, message="Tipo punto vendita non trovato")

            # Eliminazione logica del tipo punto vendita
            mongo.cx['TopFidelityCard'].tipoPuntoVendita.update_one(
                {"_id": ObjectId(idTipoPuntoVendita), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            # Controllo dei punti vendita legati al tipo punto vendita eliminato
            punti_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find(
                {"IdTipoPuntoVendita": ObjectId(idTipoPuntoVendita), "Eliminato": False})

            # Controllo delle tessere legate ai punto vendita da eliminaro
            for punto_vendita in punti_vendita:
                tessere = mongo.cx['TopFidelityCard'].tessera.find(
                    {"IdPuntoVendita": punto_vendita['_id'], "Eliminato": False})

                # Controllo dei consumatori legati alle tessere da eliminare
                for tessera in tessere:
                    consumatori = mongo.cx['TopFidelityCard'].consumatore.find(
                        {"IdTessera": tessera['_id'], "Eliminato": False})

                    # Eliminazione degli acquisti legati ai consumatori da eliminare
                    for consumatore in consumatori:
                        mongo.cx['TopFidelityCard'].acquisto.update_many(
                            {"IdConsumatore": consumatore['_id'], "Eliminato": False},
                            {"$set": {"Eliminato": True}})

                    # Eliminazione logica su consumatore
                    mongo.cx['TopFidelityCard'].consumatore.update_many(
                        {"IdTessera": tessera['_id'], "Eliminato": False},
                        {"$set": {"Eliminato": True}})
                # Eliminazione logica su tessera
                mongo.cx['TopFidelityCard'].tessera.update_many(
                    {"IdPuntoVendita": punto_vendita['_id'], "Eliminato": False},
                    {"$set": {"Eliminato": True}})
            # Eliminazione logica su puntoVendita
            mongo.cx['TopFidelityCard'].puntoVendita.update_many(
                {"IdTipoPuntoVendita": ObjectId(idTipoPuntoVendita), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            return {'message': "Tipo punto vendita e relativi documenti eliminati logicamente"}, 200

        except InvalidId:
            abort(400, message="Id tipo punto vendita non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
