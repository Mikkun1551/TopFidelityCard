from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ConsumatoreModel
from schemas import ConsumatoreSchema, UpdateConsumatoreSchema


# REQUEST CONSUMATORE
blp = Blueprint('consumatori', __name__, description='Operazioni sui consumatori')


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema(many=True))
    # Ottiene tutti i consumatori
    def get(self):
        return ConsumatoreModel.query.all()


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.response(200, ConsumatoreSchema)
    # Ottiene i dettagli di un consumatore specifico
    def get(self, idConsumatore):
        consumatore = ConsumatoreModel.query.get_or_404(idConsumatore)
        return consumatore


@blp.route('/consumatori')
class Consumatore(MethodView):
    @blp.arguments(ConsumatoreSchema)
    @blp.response(201, ConsumatoreSchema)
    # Crea un nuovo consumatore
    def post(self, dati_consumatore):
        consumatore = ConsumatoreModel(**dati_consumatore)
        try:
            db.session.add(consumatore)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Esiste già un consumatore con quella tessera")
        except SQLAlchemyError:
            abort(500, message="C'è stato un errore durante l'inserimento del consumatore")
        return consumatore


@blp.route('/consumatori/<string:idConsumatore>')
class Consumatore(MethodView):
    @blp.arguments(UpdateConsumatoreSchema)
    @blp.response(200, ConsumatoreSchema)
    # Aggiorna i dettagli di un consumatore esistente
    def put(self, dati_consumatore, idConsumatore):
        consumatore = ConsumatoreModel.query.get(idConsumatore)
        if consumatore:
            consumatore.DataTesseramento = dati_consumatore['DataTesseramento']
            consumatore.Nome = dati_consumatore['Nome']
            consumatore.Cognome = dati_consumatore['Cognome']
            consumatore.Email = dati_consumatore['Email']
            consumatore.Admin = dati_consumatore['Admin']
            consumatore.Password = dati_consumatore['Password']
            consumatore.CodiceFiscale = dati_consumatore['CodiceFiscale']
            consumatore.Indirizzo = dati_consumatore['Indirizzo']
            consumatore.Cap = dati_consumatore['Cap']
            consumatore.NumeroTelefono = dati_consumatore['NumeroTelefono']
            consumatore.IdTessera = dati_consumatore['IdTessera']
        else:
            consumatore = ConsumatoreModel(idConsumatore=idConsumatore, **dati_consumatore)
        db.session.add(consumatore)
        db.session.commit()
        return consumatore
