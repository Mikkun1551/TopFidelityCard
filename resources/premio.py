from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import PremioModel
from schemas import PremioSchema, UpdatePremioSchema


# REQUEST PREMIO
blp = Blueprint('premi', __name__, description='Operazioni sui premi')


@blp.route('/premi')
class Premio(MethodView):
    @blp.response(200, PremioSchema(many=True))
    # Ottiene tutti i premi
    def get(self):
        return PremioModel.query.all()


@blp.route('/premi/<int:idPremio>')
class Premio(MethodView):
    @blp.response(200, PremioSchema)
    # Ottiene i dettagli di un premio specifico
    def get(self, idPremio):
        premio = PremioModel.query.get_or_404(idPremio)
        return premio


@blp.route('/createPremi')
class Premio(MethodView):
    @blp.arguments(PremioSchema)
    @blp.response(201, PremioSchema)
    # Crea un nuovo premio
    def post(self, dati_premio):
        premio = PremioModel(**dati_premio)
        try:
            db.session.add(premio)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un premio con quell'url e/o codice")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento del premio")
        return premio


@blp.route('/updatePremi/<int:idPremio>')
class Premio(MethodView):
    @blp.arguments(UpdatePremioSchema)
    @blp.response(200, PremioSchema)
    # Aggiorna i dettagli di un premio esistente
    def put(self, dati_premio, idPremio):
        premio = PremioModel.query.get(idPremio)
        if premio:
            premio.Tipologia = dati_premio['Tipologia']
            premio.Descrizione = dati_premio['Descrizione']
            premio.Immagine = dati_premio['Immagine']
            premio.Url = dati_premio['Url']
            premio.Soglia = dati_premio['Soglia']
            premio.CodicePremio = dati_premio['CodicePremio']
            premio.IdCampagna = dati_premio['IdCampagna']
        else:
            premio = PremioModel(IdCampagna=idPremio, **dati_premio)
        db.session.add(premio)
        db.session.commit()
        return premio
