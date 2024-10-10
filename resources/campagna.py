from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from bson.errors import InvalidId, InvalidDocument

# Import del db
from db import mongo
from schemas import CampagnaSchema, UpdateCampagnaSchema, DeleteCampagnaSchema


# REQUEST CAMPAGNA
blp = Blueprint('campagne', __name__, description='Operazioni sulle campagne')


@blp.route('/campagne')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema(many=True))
    # Ottiene tutte le campagne
    def get(self):
        try:
            campagna = list(mongo.cx['TopFidelityCard'].campagna.find({"Eliminato": False}))
            return campagna
        except Exception as e:
            abort(400,
                  message=f"Errore non previsto: {e}")


@blp.route('/campagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema)
    # Ottiene i dettagli di una campagna specifica
    def get(self, idCampagna):
        try:
            campagna = mongo.cx['TopFidelityCard'].campagna.find_one(
                {"$and": [{"_id": ObjectId(idCampagna)}, {"Eliminato": False}]})
            if campagna is None:
                abort(404,
                      message="Campagna non trovata")
            return campagna
        except InvalidId:
            abort(400,
                  message="Id non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")


@blp.route('/createCampagne')
class Campagna(MethodView):
    @blp.arguments(CampagnaSchema)
    @blp.response(201, CampagnaSchema)
    # Crea una nuova campagna
    def post(self, dati_campagna):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"$and": [{"_id": ObjectId(dati_campagna['IdAzienda'])}, {"Eliminato": False}]})
            if not check:
                abort(404,
                      message="Azienda inserita inesistente")

            dati_campagna['Eliminato'] = False
            result = mongo.cx['TopFidelityCard'].campagna.insert_one(dati_campagna)
            campagna = mongo.cx['TopFidelityCard'].campagna.find_one(
                {"$and": [{"_id": result.inserted_id}, {"Eliminato": False}]})
            return campagna
        except TypeError:
            abort(400,
                  message=f"Id azienda inserito non valido, controlla che sia giusto")
        # Se il codice entra dentro "if not check" invece di causare abort va per except exception
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")


@blp.route('/updateCampagne/<string:idCampagna>')
class Campagna(MethodView):
    @blp.arguments(UpdateCampagnaSchema)
    @blp.response(200, CampagnaSchema)
    # Aggiorna i dettagli di una campagna esistente
    def put(self, dati_campagna, idCampagna):
        try:
            # Controllo se l'id inserito nel json della request esiste
            check = mongo.cx['TopFidelityCard'].azienda.find_one(
                {"$and": [{"_id": ObjectId(dati_campagna['IdAzienda'])}, {"Eliminato": False}]})
            if not check:
                abort(404,
                      message="Azienda inserita inesistente")

            campagna = mongo.cx['TopFidelityCard'].campagna.find_one_and_update(
                {"$and": [{"_id": ObjectId(idCampagna)}, {"Eliminato": False}]},
                {"$set": dati_campagna},
                return_document=True)
            if not campagna:
                abort(404,
                      message="Campagna non trovata")
            return campagna
        except TypeError:
            abort(400,
                  message=f"Id azienda inserito non valido, controlla che sia giusto")
        except InvalidDocument:
            abort(400,
                  message="IdAzienda non valido, riprova")
        except InvalidId:
            abort(400,
                  message="Id campagna non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")


@blp.route('/updateCampagne/delete/<string:idCampagna>')
class Campagna(MethodView):
    @blp.arguments(DeleteCampagnaSchema)
    # Cambia il flag eliminato di una campagna per cancellarlo logicamente
    def put(self, dati_campagna, idCampagna):
        try:
            if dati_campagna['Eliminato']:
                # Controllo se l'id inserito nella url esiste
                check = mongo.cx['TopFidelityCard'].campagna.find_one(
                    {"$and": [{"_id": ObjectId(idCampagna)}, {"Eliminato": False}]})
                if not check:
                    abort(404,
                          message="Campagna non trovata")

                # Eliminazione logica
                mongo.cx['TopFidelityCard'].campagna.update_one(
                    {"$and": [{"_id": ObjectId(idCampagna)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})

                # Eliminazione "cascade" su premio
                mongo.cx['TopFidelityCard'].premio.update_many(
                    {"$and": [{"IdCampagna": ObjectId(idCampagna)}, {"Eliminato": False}]},
                    {"$set": {"Eliminato": True}})

                return {'message': "Campagna e relativi premi eliminati logicamente"}, 200
            else:
                abort(404,
                      message="Impostare il parametro eliminato su true per usare questa procedura")
        except InvalidId:
            abort(400,
                  message="Id campagna non valido, riprova")
        # except Exception as e:
        #     abort(400,
        #           message=f"Errore non previsto: {e}")
