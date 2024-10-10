from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument
from werkzeug.exceptions import HTTPException

# Import del db
from db import mongo
from schemas import PremioSchema, UpdatePremioSchema, DeletePremioSchema


# REQUEST PREMIO
blp = Blueprint('premi', __name__, description='Operazioni sui premi')


@blp.route('/premi')
class Premio(MethodView):
    @blp.response(200, PremioSchema(many=True))
    # Ottiene tutti i premi
    def get(self):
        try:
            premio = list(mongo.cx['TopFidelityCard'].premio.find({"Eliminato": False}))
            return premio
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/premi/<string:idPremio>')
class Premio(MethodView):
    @blp.response(200, PremioSchema)
    # Ottiene i dettagli di un premio specifico
    def get(self, idPremio):
        try:
            premio = mongo.cx['TopFidelityCard'].premio.find_one(
                {"_id": ObjectId(idPremio), "Eliminato": False})
            if premio is None:
                abort(404, message="Premio non trovato")
            return premio
        except InvalidId:
            abort(400, message="Id non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/createPremi')
class Premio(MethodView):
    @blp.arguments(PremioSchema)
    @blp.response(201, PremioSchema)
    # Crea un nuovo premio
    def post(self, dati_premio):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].campagna.find_one(
                {"_id": ObjectId(dati_premio['IdCampagna']), "Eliminato": False})
            if not check:
                abort(404, message="Campagna inserita inesistente")

            dati_premio['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].premio.insert_one(dati_premio)
            premio = mongo.cx['TopFidelityCard'].premio.find_one(
                {"_id": result.inserted_id, "Eliminato": False})
            return premio
        except TypeError:
            abort(400, message=f"Id campagna inserito non valido, controlla che sia giusto")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/updatePremi/<string:idPremio>')
class Premio(MethodView):
    @blp.arguments(UpdatePremioSchema)
    @blp.response(200, PremioSchema)
    # Aggiorna i dettagli di un premio esistente
    def put(self, dati_premio, idPremio):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].campagna.find_one(
                {"_id": ObjectId(dati_premio['IdCampagna']), "Eliminato": False})
            if not check:
                abort(404, message="Campagna inserita inesistente")

            premio = mongo.cx['TopFidelityCard'].premio.find_one_and_update(
                {"_id": ObjectId(idPremio), "Eliminato": False},
                {"$set": dati_premio},
                return_document=True)
            if not premio:
                abort(404, message="Premio non trovato")
            return premio
        except TypeError:
            abort(400, message=f"Id campagna inserito non valido, controlla che sia giusto")
        except InvalidDocument:
            abort(400, message="IdCampagna non valido, riprova")
        except InvalidId:
            abort(400, message="Id premio non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")


@blp.route('/updatePremi/delete/<string:idPremio>')
class Premio(MethodView):
    @blp.arguments(DeletePremioSchema)
    # Cambia il flag eliminato di un premio per cancellarlo logicamente
    def put(self, dati_premio, idPremio):
        try:
            if dati_premio['Eliminato']:
                # Controllo se l'id inserito nella url esiste
                check = mongo.cx['TopFidelityCard'].premio.find_one(
                    {"_id": ObjectId(idPremio), "Eliminato": False})
                if not check:
                    abort(404, message="Premio non trovato")

                # Eliminazione logica
                mongo.cx['TopFidelityCard'].premio.update_one(
                    {"_id": ObjectId(idPremio), "Eliminato": False},
                    {"$set": {"Eliminato": True}})

                return {'message': "Premio eliminato logicamente"}, 200
            else:
                abort(404, message="Impostare il parametro eliminato su true per usare questa procedura")
        except InvalidId:
            abort(400, message="Id premio non valido, riprova")
        # Necessario per evitare che if not azienda vada per l'exception generica
        except HTTPException:
            raise
        except Exception as e:
            abort(500, message=f"Errore non previsto: {e}")
