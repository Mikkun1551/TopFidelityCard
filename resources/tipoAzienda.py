from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TipoAziendaModel
from schemas import TipoAziendaSchema, UpdateTipoAziendaSchema

# REQUEST TIPO AZIENDA
blp = Blueprint('tipiAzienda', __name__, description='Operazioni sui tipi azienda')


@blp.route('/apiTipiAzienda/tipiAzienda')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema(many=True))
    # Ottiene tutti i tipi di azienda
    def get(self):
        return TipoAziendaModel.query.all()


@blp.route('/apiTipiAzienda/tipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.response(200, TipoAziendaSchema)
    # Ottiene i dettagli di un tipo di azienda specifico
    def get(self, idTipoAzienda):
        azienda = TipoAziendaModel.query.get_or_404(idTipoAzienda)
        return azienda


@blp.route('/apiTipiAzienda/createTipiAzienda')
class TipoAzienda(MethodView):
    @blp.arguments(TipoAziendaSchema)
    @blp.response(201, TipoAziendaSchema)
    # Crea un nuovo tipo di azienda
    def post(self, dati_t_azienda):
        t_azienda = TipoAziendaModel(**dati_t_azienda)
        try:
            db.session.add(t_azienda)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un tipo azienda con quel nome")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento del tipo azienda")
        return t_azienda


@blp.route('/apiTipiAzienda/updateTipiAzienda/<int:idTipoAzienda>')
class TipoAzienda(MethodView):
    @blp.arguments(UpdateTipoAziendaSchema)
    @blp.response(200, TipoAziendaSchema)
    # Aggiorna i dettagli di un tipo di azienda esistente
    def put(self, dati_t_azienda, idTipoAzienda):
        t_azienda = TipoAziendaModel.query.get(idTipoAzienda)
        if t_azienda:
            t_azienda.Categoria = dati_t_azienda['Categoria']
            t_azienda.Descrizione = dati_t_azienda['Descrizione']
        else:
            t_azienda = TipoAziendaModel(IdTipoAzienda=idTipoAzienda, **dati_t_azienda)
        db.session.add(t_azienda)
        db.session.commit()
        return t_azienda
