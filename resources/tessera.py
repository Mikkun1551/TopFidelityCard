from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TesseraModel
from schemas import TesseraSchema, UpdateTesseraSchema


# REQUEST TESSERA
blp = Blueprint('tessere', __name__, description='Operazioni sulle tessere')


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema(many=True))
    # Ottiene tutte le tessere
    def get(self):
        return TesseraModel.query.all()


@blp.route('/tessere_gruppo/<int:idTessera>')
class Tessera(MethodView):
    @blp.response(200, TesseraSchema)
    # Ottiene i dettagli di una tessera specifica
    def get(self, idTessera):
        tessera = TesseraModel.query.get_or_404(idTessera)
        return tessera


@blp.route('/tessere_gruppo')
class Tessera(MethodView):
    @blp.arguments(TesseraSchema)
    @blp.response(201, TesseraSchema)
    # Crea una nuova tessera
    def post(self, dati_tessera):
        tessera = TesseraModel(**dati_tessera)
        try:
            db.session.add(tessera)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già una tessera con quel codice")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento della tessera")
        return tessera


@blp.route('/tessere_gruppo/<int:idTessera>')
class Tessera(MethodView):
    @blp.arguments(UpdateTesseraSchema)
    @blp.response(200, TesseraSchema)
    # Aggiorna i dettagli di una tessera esistente
    def put(self, dati_tessera, idTessera):
        tessera = TesseraModel.query.get(idTessera)
        if tessera:
            tessera.CodiceTessera = dati_tessera['CodiceTessera']
            tessera.DataCreazione = dati_tessera['DataCreazione']
            tessera.DataScadenza = dati_tessera['DataScadenza']
            tessera.IdPuntoVendita = dati_tessera['IdPuntoVendita']
        else:
            tessera = TesseraModel(IdTessera=idTessera, **dati_tessera)
        db.session.add(tessera)
        db.session.commit()
        return tessera
