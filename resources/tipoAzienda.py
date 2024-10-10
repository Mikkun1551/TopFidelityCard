from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId

# Import del db
from db import mongo
from schemas import TipoAziendaSchema, UpdateTipoAziendaSchema, DeleteTipoAziendaSchema


# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')


@blp.route('/apiTipiAzienda/tipiAzienda')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema(many=True))
    # Ottiene tutti i tipi di azienda
    def get(self):
        try:
            t_azienda = list(mongo.cx['TopFidelityCard'].tipoAzienda.find({"Eliminato": False}))
            return t_azienda
        except Exception as e:
            abort(400,
                  message=f"Errore non previsto: {e}")


@blp.route('/apiTipiAzienda/tipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema)
    # Ottiene i dettagli di un tipo di azienda specifico
    def get(self, idTipoAzienda):
        try:
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one(
                {"$and": [{"_id": ObjectId(idTipoAzienda)}, {"Eliminato": False}]})
            if t_azienda is None:
                abort(404,
                      message="Tipo azienda non trovato")
            return t_azienda
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(TipoAziendaSchema)
    @blp.response(201, TipoAziendaSchema)
    # Crea un nuovo tipo di azienda
    def post(self, dati_t_azienda):
        try:
            dati_t_azienda['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].tipoAzienda.insert_one(dati_t_azienda)
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one(
                {"$and": [{"_id": result.inserted_id}, {"Eliminato": False}]})
            return t_azienda
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except Exception as e:
            abort(400,
                  message=f"Errore non previsto: {e}")


@blp.route('/apiTipiAzienda/updateTipiAzienda/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, TipoAziendaSchema)
    # Aggiorna i dettagli di un tipo di azienda esistente
    def put(self, dati_t_azienda, idTipoAzienda):
        try:
            t_azienda = mongo.cx['TopFidelityCard'].tipoAzienda.find_one_and_update(
                {"$and": [{"_id": ObjectId(idTipoAzienda)}, {"Eliminato": False}]},
                {"$set": dati_t_azienda},
                return_document=True)
            if not t_azienda:
                abort(404,
                      message="Tipo azienda non trovato")
            return t_azienda
        except DuplicateKeyError as e:
            key_pattern = e.details.get("keyPattern")
            field_error = list(key_pattern.keys())
            abort(400,
                  message=f"Richiesta non valida, '{field_error[0]}' già esistente")
        except InvalidId:
            abort(400,
                  message="Id tipo azienda non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")


@blp.route('/apiTipiAzienda/updateTipiAzienda/delete/<string:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(DeleteTipoAziendaSchema)
    # Cambia il flag eliminato di un tipo azienda per cancellarlo logicamente
    def put(self, dati_t_azienda, idTipoAzienda):
        try:
            if dati_t_azienda['Eliminato']:
                # Controllo se l'id inserito nella url esiste
                check = mongo.cx['TopFidelityCard'].tipoAzienda.find_one(
                    {"$and": [{"_id": ObjectId(idTipoAzienda)}, {"Eliminato": False}]})
                if not check:
                    abort(404,
                          message="Tipo azienda non trovato")

                # Eliminazione logica
                mongo.cx['TopFidelityCard'].tipoAzienda.update_one(
                    {"$and": [{"_id": ObjectId(idTipoAzienda)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})

                # Controllo delle aziende legate al tipo azienda eliminato
                aziende = mongo.cx['TopFidelityCard'].azienda.find(
                    {"$and": [{"IdTipoAzienda": ObjectId(idTipoAzienda)}, {"Eliminato": False}]})

                # Controllo delle campagne e punti vendita legati alle aziende da eliminare
                for azienda in aziende:
                    # 1: Branch: Controllo delle campagne legate alle aziende da eliminare
                    campagne = mongo.cx['TopFidelityCard'].campagna.find(
                        {"$and": [{"IdAzienda": azienda['_id']}, {"Eliminato": False}]})

                    # Eliminazione dei premi legati alle campagne da eliminare
                    for campagna in campagne:
                        mongo.cx['TopFidelityCard'].premio.update_many(
                            {"$and": [{"IdCampagna": campagna['_id']}, {"Eliminato": False}]},
                            {"$set": {"Eliminato": True}})

                    # Eliminazione "cascade" su campagna
                    mongo.cx['TopFidelityCard'].campagna.update_many(
                        {"$and": [{"IdAzienda": azienda['_id']}, {"Eliminato": False}]},
                        {"$set": {"Eliminato": True}})

                    # 2. Branch: Controllo dei punti vendita legati all'azienda eliminata
                    punti_vendita = mongo.cx['TopFidelityCard'].puntoVendita.find(
                        {"$and": [{"IdAzienda": azienda['_id']}, {"Eliminato": False}]})

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
                        {"$and": [{"IdAzienda": azienda['_id']}, {"Eliminato": False}]},
                        {"$set": {"Eliminato": True}})

                # Eliminazione "cascade" su azienda
                mongo.cx['TopFidelityCard'].azienda.update_many(
                    {"$and": [{"IdTipoAzienda": ObjectId(idTipoAzienda)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})

                return {'message': "Azienda e relativi documenti eliminati logicamente"}, 200
            else:
                abort(404,
                      message="Impostare il parametro eliminato su true per usare questa procedura")
        except InvalidId:
            abort(400,
                  message="Id tipo azienda non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")
