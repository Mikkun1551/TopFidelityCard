from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CampagnaModel
from schemas import CampagnaSchema, UpdateCampagnaSchema


# REQUEST CAMPAGNA
blp = Blueprint('campagne', __name__, description='Operazioni sulle campagne')


@blp.route('/campagne')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema(many=True))
    # Ottiene tutte le campagne
    def get(self):
        return CampagnaModel.query.all()


@blp.route('/campagne/<int:idCampagna>')
class Campagna(MethodView):
    @blp.response(200, CampagnaSchema)
    # Ottiene i dettagli di una campagna specifica
    def get(self, idCampagna):
        campagna = CampagnaModel.query.get_or_404(idCampagna)
        return campagna


@blp.route('/createCampagne')
class Campagna(MethodView):
    @blp.arguments(CampagnaSchema)
    @blp.response(201, CampagnaSchema)
    # Crea una nuova campagna
    def post(self, dati_campagna):
        campagna = CampagnaModel(**dati_campagna)
        try:
            db.session.add(campagna)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già una campagna con quel nome")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento della campagna")
        return campagna


@blp.route('/updateCampagne/<int:idCampagna>')
class Campagna(MethodView):
    @blp.arguments(UpdateCampagnaSchema)
    @blp.response(200, CampagnaSchema)
    # Aggiorna i dettagli di una campagna esistente
    def put(self, dati_campagna, idCampagna):
        campagna = CampagnaModel.query.get(idCampagna)
        if campagna:
            campagna.Nome = dati_campagna['Nome']
            campagna.DataInizio = dati_campagna['DataInizio']
            campagna.DataFine = dati_campagna['DataFine']
            campagna.ConversionePuntiEuro = dati_campagna['ConversionePuntiEuro']
            campagna.IdAzienda = dati_campagna['IdAzienda']
        else:
            campagna = CampagnaModel(IdCampagna=idCampagna, **dati_campagna)
        db.session.add(campagna)
        db.session.commit()
        return campagna
