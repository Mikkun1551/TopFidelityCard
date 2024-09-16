from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import AziendaModel
from schemas import AziendaSchema, UpdateAziendaSchema

# REQUEST AZIENDA
blp = Blueprint('aziende', __name__, description='Operazioni sulle aziende')


@blp.route('/apiAzienda/aziende')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema(many=True))
    # Ottiene tutte le azienda
    def get(self):
        return AziendaModel.query.all()


@blp.route('/apiAzienda/aziende/<int:idAzienda>')
class Azienda(MethodView):
    @blp.response(200, AziendaSchema)
    # Ottiene i dettagli di un'azienda specifica
    def get(self, idAzienda):
        azienda = AziendaModel.query.get_or_404(idAzienda)
        return azienda


@blp.route('/apiAzienda/createAziende')
class Azienda(MethodView):
    @blp.arguments(AziendaSchema)
    @blp.response(201, AziendaSchema)
    # Crea una nuova azienda
    def post(self, dati_azienda):
        azienda = AziendaModel(**dati_azienda)
        try:
            db.session.add(azienda)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un'azienda con quel nome")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento dell'azienda")
        return azienda


@blp.route('/apiAzienda/updateAziende/<int:idAzienda>')
class Azienda(MethodView):
    @blp.arguments(UpdateAziendaSchema)
    @blp.response(200, AziendaSchema)
    # Aggiorna i dettagli di un'azienda esistente
    def put(self, dati_azienda, idAzienda):
        azienda = AziendaModel.query.get(idAzienda)
        if azienda:
            azienda.Nome = dati_azienda['Nome']
            azienda.Regione = dati_azienda['Regione']
            azienda.Citta = dati_azienda['Citta']
            azienda.Cap = dati_azienda['Cap']
            azienda.P_IVA = dati_azienda['P_IVA']
            azienda.IdTipoAzienda = dati_azienda['IdTipoAzienda']
        else:
            azienda = AziendaModel(IdAzienda=idAzienda, **dati_azienda)
        db.session.add(azienda)
        db.session.commit()
        return azienda
