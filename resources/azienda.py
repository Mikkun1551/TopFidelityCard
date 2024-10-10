from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import AziendaSchema, UpdateAziendaSchema, DeleteAziendaSchema


# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')


@blp.route('/apiAzienda/aziende')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema(many=True))
    # Ottiene tutte le azienda
    def get(self):
        try:
            azienda = list(mongo.cx['TopFidelityCard'].azienda.find({"Eliminato": False}))
            return azienda
        except Exception as e:
            abort(400, message=f"Errore non previsto: {e}")


@blp.route('/apiAzienda/aziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema)
    # Ottiene i dettagli di un'azienda specifica
    def get(self, idAzienda):
        try:
            azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"$and": [{"_id": ObjectId(idAzienda)}, {"Eliminato": False}]})
            if not azienda:
                abort(404, message="Azienda non trovata")
            return azienda
        except InvalidId:
            abort(400, message="Id inserito non valido, riprova con un id giusto")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(AziendaSchema)
    @blp.response(201, AziendaSchema)
    # Crea una nuova azienda
    def post(self, dati_azienda):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].tipoAzienda.find_one(
                {"$and": [{"_id": ObjectId(dati_azienda['IdTipoAzienda'])}, {"Eliminato": False}]})
            if not check:
                abort(404, message="Tipo azienda inserito inesistente")

            dati_azienda['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].azienda.insert_one(dati_azienda)
            azienda = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"$and": [{"_id": result.inserted_id}, {"Eliminato": False}]})
            return azienda
        except TypeError:
            abort(400, message=f"Id tipo azienda inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400, message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/apiAzienda/updateAziende/<string:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    @blp.response(200, AziendaSchema)
    # Aggiorna i dettagli di un'azienda esistente
    def put(self, dati_azienda, idAzienda):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].tipoAzienda.find_one(
                {"$and": [{"_id": ObjectId(dati_azienda['IdTipoAzienda'])}, {"Eliminato": False}]})
            if not check:
                abort(404,
                      message="Tipo azienda inserito inesistente")

            azienda = mongo.cx['TopFidelityCard'].azienda.find_one_and_update(
                {"$and": [{"_id": ObjectId(idAzienda)}, {"Eliminato": False}]},
                {"$set": dati_azienda},
                return_document=True)
            if not azienda:
                abort(404,
                      message="Azienda non trovata")
            return azienda
        except TypeError:
            abort(400,
                  message=f"Id tipo azienda inserito non valido, controlla che sia giusto")
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidDocument:
            abort(400,
                  message="IdTipoAzienda non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id azienda non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/apiAzienda/updateAziende/delete/<string:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(DeleteAziendaSchema)
    # Cambia il flag eliminato di un'azienda per cancellarlo logicamente
    def put(self, dati_azienda, idAzienda):
        try:
            if dati_azienda['Eliminato']:
                # Controllo se l'id inserito nella url esiste
                check = mongo.cx['TopFidelityCard'].azienda.find_one(
                    {"$and": [{"_id": ObjectId(idAzienda)}, {"Eliminato": False}]})
                if not check:
                    abort(404,
                          message="Azienda non trovata")

                # Eliminazione logica
                mongo.cx['TopFidelityCard'].azienda.update_one(
                    {"$and": [{"_id": ObjectId(idAzienda)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})


                # 1: Branch: Controllo delle campagne legate all'azienda eliminata
                campagne = mongo.cx['TopFidelityCard'].campagna.find(
                    {"$and": [{"IdAzienda": ObjectId(idAzienda)}, {"Eliminato": False}]})

                # Eliminazione dei premi legati alle campagne da eliminare
                for campagna in campagne:
                    mongo.cx['TopFidelityCard'].premio.update_many(
                        {"$and": [{"IdCampagna": campagna['_id']}, {"Eliminato": False}]},
                        {"$set": {"Eliminato": True}})

                # Eliminazione "cascade" su campagna
                mongo.cx['TopFidelityCard'].campagna.update_many(
                    {"$and": [{"IdAzienda": ObjectId(idAzienda)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})



                # 2. Branch: Controllo dei punti vendita legati all'azienda eliminata
                punti_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find(
                    {"$and": [{"IdAzienda": ObjectId(idAzienda)}, {"Eliminato": False}]})

                # Controllo delle tessere legate al punto vendita eliminato
                for punto_vendita in punti_vendita:
                    tessere = mongo.cx['TopFidelityCard'].tessera.find(
                        {"$and": [{"IdPuntoVendita": punto_vendita['_id']}, {"Eliminato": False}]})

                    # Controllo dei consumatori legati alle tessere da eliminare
                    for tessera in tessere:
                        consumatori = mongo.cx['TopFidelityCard'].consumatore.find(
                            {"$and": [{"IdTessera": tessera['_id']}, {"Eliminato": False}]})

                        # Eliminazione degli acquisti legati ai consumatori da eliminare
                        for consumatore in consumatori:
                            mongo.cx['TopFidelityCard'].acquisto.update_many(
                                {"$and": [{"IdConsumatore": consumatore['_id']}, {"Eliminato": False}]},
                                {"$set": {"Eliminato": True}})

                        # Eliminazione "cascade" su consumatore
                        mongo.cx['TopFidelityCard'].consumatore.update_many(
                            {"$and": [{"IdTessera": tessera['_id']}, {"Eliminato": False}]},
                            {"$set": {"Eliminato": True}})

                    # Eliminazione "cascade" su tessera
                    mongo.cx['TopFidelityCard'].tessera.update_many(
                        {"$and": [{"IdPuntoVendita": punto_vendita['_id']}, {"Eliminato": False}]},
                        {"$set": {"Eliminato": True}})

                # Eliminazione "cascade" su puntoVendita
                mongo.cx['TopFidelityCard'].puntoVendita.update_many(
                    {"$and": [{"IdAzienda": ObjectId(idAzienda)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})


                return {'message': "Azienda e relativi documenti eliminati logicamente"}, 200
            else:
                abort(404,
                      message="Impostare il parametro eliminato su true per usare questa procedura")
        except InvalidId:
            abort(400,
                  message="Id punto vendita non valido, riprova")
        # Necessario per evitare che if not check vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
