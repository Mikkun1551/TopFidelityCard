from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import PuntoVenditaSchema, UpdatePuntoVenditaSchema, DeletePuntoVenditaSchema


# REQUEST PUNTO VENDITA
blp = Blueprint('puntiVendita', __name__, description='Operazioni sui punti vendita')


@blp.route('/PuntoVendita')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema(many=True))
    # Ottiene tutti i punti vendita
    def get(self):
        try:
            punto_vendita = list(mongo.cx['TopFidelityCard'].puntoVendita.find({"Eliminato": False}))
            return punto_vendita
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


    @blp.arguments(PuntoVenditaSchema)
    @blp.response(201, PuntoVenditaSchema)
    # Crea un nuovo punto vendita
    def post(self, dati_punto_vendita):
        try:
            # Controllo se gli id inseriti nel json della request esistono
            check_azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdAzienda']), "Eliminato": False})
            if not check_azienda:
                abort(404, message="Azienda inserita inesistente")
            check_t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdTipoPuntoVendita']), "Eliminato": False})
            if not check_t_punto_vendita:
                abort(404, message="Tipo punto vendita inserito inesistente")

            dati_punto_vendita['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].puntoVendita.insert_one(dati_punto_vendita)
            dati_punto_vendita['_id'] = result.inserted_id
            return dati_punto_vendita
        except TypeError:
            abort(400, message=f"Uno o entrambi gli id inseriti non sono validi, controlla e riprova")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        # Necessario per evitare che gli if not check vadano per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/PuntoVendita/<string:idPuntoVendita>')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema)
    # Ottiene i dettagli di un punto vendita specifico
    def get(self, idPuntoVendita):
        try:
            punto_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find_one(
                {"_id": ObjectId(idPuntoVendita), "Eliminato": False})
            if not punto_vendita:
                abort(404, message="Punto vendita non trovato")
            return punto_vendita
        except InvalidId:
            abort(400, message="Id inserito non valido, riprova con un id giusto")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


    @blp.arguments(UpdatePuntoVenditaSchema)
    @blp.response(200, PuntoVenditaSchema)
    # Aggiorna i dettagli di un punto vendita esistente
    def put(self, dati_punto_vendita, idPuntoVendita):
        try:
            # Controllo se gli id inseriti nel json della request esistono
            check_azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdAzienda']), "Eliminato": False})
            if not check_azienda:
                abort(404, message="Azienda inserita inesistente")
            check_t_punto_vendita = mongo.cx['TopFidelityCard'].tipoPuntoVendita.find_one(
                {"_id": ObjectId(dati_punto_vendita['IdTipoPuntoVendita']), "Eliminato": False})
            if not check_t_punto_vendita:
                abort(404, message="Tipo punto vendita inserito inesistente")

            punto_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find_one_and_update(
                {"_id": ObjectId(idPuntoVendita), "Eliminato": False},
                {"$set": dati_punto_vendita},
                return_document=True)
            if not punto_vendita:
                abort(404, message="Punto vendita non trovato")
            return punto_vendita
        except TypeError:
            abort(400, message=f"Uno o entrambi gli id inseriti non sono validi, controlla e riprova")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidDocument:
            abort(400, message="IdAzienda e/o idTipoPuntoVendita non valido/i, riprova")
        except InvalidId:
            abort(400, message="Id punto vendita non valido, riprova")
        # Necessario per evitare che gli if not vadano per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/PuntoVendita/delete/<string:idPuntoVendita>')
class PuntoVendita(MethodView):
    @blp.arguments(DeletePuntoVenditaSchema)
    # Cambia il flag eliminato di un punto vendita per cancellarlo logicamente
    def put(self, dati_punto_vendita, idPuntoVendita):
        try:
            # Controllo che la procedura venga avviata
            if not dati_punto_vendita['Eliminato']:
                abort(404, message="Impostare il parametro eliminato su true per usare questa procedura")

            # Controllo se l'id inserito nella url esiste
            check = mongo.cx['TopFidelityCard'].puntoVendita.find_one(
                {"_id": ObjectId(idPuntoVendita), "Eliminato": False})
            if not check:
                abort(404, message="Punto vendita non trovato")

            # Eliminazione logica del punto vendita
            mongo.cx['TopFidelityCard'].puntoVendita.update_one(
                {"_id": ObjectId(idPuntoVendita), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            # Controllo delle tessere legate al punto vendita eliminato
            tessere = mongo.cx['TopFidelityCard'].tessera.find(
                {"IdPuntoVendita": ObjectId(idPuntoVendita), "Eliminato": False})

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
                {"IdPuntoVendita": ObjectId(idPuntoVendita), "Eliminato": False},
                {"$set": {"Eliminato": True}})
            return {'message': "Punto vendita e relativi documenti eliminati logicamente"}, 200

        except InvalidId:
            abort(400, message="Id punto vendita non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
