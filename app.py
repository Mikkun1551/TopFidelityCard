import os
from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.azienda import blp as AziendaBlueprint
from resources.tipoAzienda import blp as TipoAziendaBlueprint
from resources.puntoVendita import blp as PuntoVenditaBlueprint
from resources.tipoPuntoVendita import blp as TipoPuntoVenditaBlueprint
from resources.campagna import blp as CampagnaBlueprint
from resources.premio import blp as PremioBlueprint
from resources.tessera import blp as TesseraBlueprint
from resources.consumatore import blp as ConsumatoreBlueprint
from resources.acquisto import blp as AcquistoBlueprint


# Creazione di una flask app
def create_app(db_url=None):
    app = Flask(__name__)

    # Propagare le eccezioni delle estensioni di flask al main app per leggerle
    app.config['PROPAGATE_EXCEPTIONS'] = True
    # Il titolo dell'api
    app.config['API_TITLE'] = 'TopFidelityCard'
    # Versione corrente dell'api
    app.config['API_VERSION'] = 'v1'
    # Versione di openapi, uno standard per la documentazione api
    app.config['OPENAPI_VERSION'] = '3.0.3'
    # La posizione della root dell'api, visto che tutte le request
    # iniziano con / la root è quella
    app.config['OPENAPI_URL_PREFIX'] = '/'
    # Settare il path per la documentazione dell'api tramite swagger
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    # Settare l'url da dove prendere la documentazione dell'api
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    # Settare url del database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    # Configurazione per le track modifications di SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Inizializazione collegamento sqlalchemy e la flask app
    db.init_app(app)

    # Connessione tra flask smorest alla flask app
    api = Api(app)

    # Creazione db prima della prima request
    with app.app_context():
        db.create_all()

    # Import dei blueprint da resources
    api.register_blueprint(AziendaBlueprint)
    api.register_blueprint(TipoAziendaBlueprint)
    api.register_blueprint(PuntoVenditaBlueprint)
    api.register_blueprint(TipoPuntoVenditaBlueprint)
    api.register_blueprint(CampagnaBlueprint)
    api.register_blueprint(PremioBlueprint)
    api.register_blueprint(TesseraBlueprint)
    api.register_blueprint(ConsumatoreBlueprint)
    api.register_blueprint(AcquistoBlueprint)

    return app
