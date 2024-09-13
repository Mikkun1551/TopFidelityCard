from flask import Flask
from flask_smorest import Api
from resources.azienda import blp as AziendaBlueprint
from resources.tipoAzienda import blp as TipoAziendaBlueprint

# Creazione di una flask app
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

# Connessione tra flask smorest alla flask app
api = Api(app)

# Import dei blueprint da resources
api.register_blueprint(AziendaBlueprint)
api.register_blueprint(TipoAziendaBlueprint)
