from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import PuntoVenditaModel
from schemas import PuntoVenditaSchema, UpdatePuntoVenditaSchema


# REQUEST PUNTO VENDITA
blp = Blueprint('puntiVendita', __name__, description='Operazioni sui punti vendita')


@blp.route('/PuntoVendita')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema(many=True))
    # Ottiene tutti i punti vendita
    def get(self):
        return PuntoVenditaModel.query.all()

    @blp.arguments(PuntoVenditaSchema)
    @blp.response(201, PuntoVenditaSchema)
    # Crea un nuovo punto vendita
    def post(self, dati_punto_vendita):
        punto_vendita = PuntoVenditaModel(**dati_punto_vendita)
        try:
            db.session.add(punto_vendita)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un punto vendita con quel nome")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento del punto vendita")
        return punto_vendita


@blp.route('/PuntoVendita/<int:idPuntoVendita>')
class PuntoVendita(MethodView):
    @blp.response(200, PuntoVenditaSchema)
    # Ottiene i dettagli di un punto vendita specifico
    def get(self, idPuntoVendita):
        punto_vendita = PuntoVenditaModel.query.get_or_404(idPuntoVendita)
        return punto_vendita

    @blp.arguments(UpdatePuntoVenditaSchema)
    @blp.response(200, PuntoVenditaSchema)
    # Aggiorna i dettagli di un punto vendita esistente
    def put(self, dati_punto_vendita, idPuntoVendita):
        punto_vendita = PuntoVenditaModel.query.get(idPuntoVendita)
        if punto_vendita:
            punto_vendita.Nome = dati_punto_vendita['Nome']
            punto_vendita.Indirizzo = dati_punto_vendita['Indirizzo']
            punto_vendita.Citta = dati_punto_vendita['Citta']
            punto_vendita.Cap = dati_punto_vendita['Cap']
            punto_vendita.IdTipoPuntoVendita = dati_punto_vendita['IdTipoPuntoVendita']
            punto_vendita.IdAzienda = dati_punto_vendita['IdAzienda']
        else:
            punto_vendita = PuntoVenditaModel(IdPuntoVendita=idPuntoVendita, **dati_punto_vendita)
        db.session.add(punto_vendita)
        db.session.commit()
        return punto_vendita
