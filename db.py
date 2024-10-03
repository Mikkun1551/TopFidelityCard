from flask_pymongo import PyMongo

# Inizializzazione del client PyMongo
mongo = PyMongo()

def init_db(app):
    # Configurazione della URI MongoDB
    app.config['MONGO_URI'] = (
    'mongodb+srv://admin:qIzjfYMqPaG4fvIM@cluster0.0eqpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # Inizializzazione Mongo client con la flask app
    mongo.init_app(app)
