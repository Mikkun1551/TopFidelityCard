from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TipoPuntoVenditaModel
from schemas import TipoPuntoVenditaSchema, UpdateTipoPuntoVenditaSchema


# REQUEST TIPO PUNTO VENDITA
blp = Blueprint('tipiPuntoVendita', __name__, description='Operazioni sui tipi punto vendita')


@blp.route('/tipoPuntoVendita')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema(many=True))
    # Ottiene tutti i tipi di punto vendita
    def get(self):
        return TipoPuntoVenditaModel.query.all()

    @blp.arguments(TipoPuntoVenditaSchema)
    @blp.response(201, TipoPuntoVenditaSchema)
    # Crea un nuovo tipo di punto vendita
    def post(self, dati_t_punto_vendita):
        t_punto_vendita = TipoPuntoVenditaModel(**dati_t_punto_vendita)
        try:
            db.session.add(t_punto_vendita)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un tipo punto vendita con quel nome")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento del tipo punto vendita")
        return t_punto_vendita


@blp.route('/tipoPuntoVendita/<int:idTipoPuntoVendita>')
class TipoPuntoVendita(MethodView):
    @blp.response(200, TipoPuntoVenditaSchema)
    # Ottiene i dettagli di un tipo punto vendita specifico
    def get(self, idTipoPuntoVendita):
        t_punto_vendita = TipoPuntoVenditaModel.query.get_or_404(idTipoPuntoVendita)
        return t_punto_vendita

    @blp.arguments(UpdateTipoPuntoVenditaSchema)
    @blp.response(200, TipoPuntoVenditaSchema)
    # Aggiorna i dettagli di un tipo punto vendita esistente
    def put(self, dati_t_punto_vendita, idTipoPuntoVendita):
        t_punto_vendita = TipoPuntoVenditaModel.query.get(idTipoPuntoVendita)
        if t_punto_vendita:
            t_punto_vendita.Nome = dati_t_punto_vendita['Nome']
            t_punto_vendita.Descrizione = dati_t_punto_vendita['Descrizione']
        else:
            t_punto_vendita = TipoPuntoVenditaModel(IdTipoPuntoVendita=idTipoPuntoVendita, **dati_t_punto_vendita)
        db.session.add(t_punto_vendita)
        db.session.commit()
        return t_punto_vendita
