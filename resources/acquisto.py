from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import AcquistoModel
from schemas import AcquistoSchema, UpdateAcquistoSchema


# REQUEST ACQUISTO
blp = Blueprint('acquisti', __name__, description='Operazioni sugli acquisti')


@blp.route('/acquisti')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema(many=True))
    # Ottiene tutti gli acquisti
    def get(self):
        return AcquistoModel.query.all()


@blp.route('/acquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.response(200, AcquistoSchema)
    # Ottiene i dettagli di un'acquisto specifico
    def get(self, idAcquisto):
        acquisto = AcquistoModel.query.get_or_404(idAcquisto)
        return acquisto


@blp.route('/createAcquisti')
class Acquisto(MethodView):
    @blp.arguments(AcquistoSchema)
    @blp.response(201, AcquistoSchema)
    # Crea un nuovo acquisto
    def post(self, dati_acquisto):
        acquisto = AcquistoModel(**dati_acquisto)
        try:
            db.session.add(acquisto)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Errore sconosciuto ")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento dell'acquisto'")
        return acquisto


@blp.route('/updateAcquisti/<int:idAcquisto>')
class Acquisto(MethodView):
    @blp.arguments(UpdateAcquistoSchema)
    @blp.response(200, AcquistoSchema)
    # Aggiorna i dettagli di un'acquisto esistente
    def put(self, dati_acquisto, idAcquisto):
        acquisto = AcquistoModel.query.get(idAcquisto)
        if acquisto:
            acquisto.DataAcquisto = dati_acquisto['DataAcquisto']
            acquisto.PuntiAcquisiti = dati_acquisto['PuntiAcquisiti']
            acquisto.IdConsumatore = dati_acquisto['IdConsumatore']
        else:
            acquisto = AcquistoModel(IdAcquisto=idAcquisto, **dati_acquisto)
        db.session.add(acquisto)
        db.session.commit()
        return acquisto
