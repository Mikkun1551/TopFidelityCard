import secrets
import string
from db import db
from sqlalchemy import event
from sqlalchemy.orm import Session


# Funzione per generare una stringa randomica per idConsumatore
def generazione_stringa_random(lunghezza=12):
    caratteri = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caratteri) for _ in range(lunghezza))


# Funzione per assicurarsi che la stringa creata sia unique
def generazione_stringa_unique(mapper, connection, target): # anche se non usati non rimuovere mapper e connection
    session = Session.object_session(target)
    while True:
        new_id = generazione_stringa_random()
        # Controllo che l'id generato sia unique
        if not session.query(ConsumatoreModel).filter_by(IdConsumatore=new_id).first():
            target.IdConsumatore = new_id
            break


class ConsumatoreModel(db.Model):
    __tablename__ = "Consumatore"

    IdConsumatore = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    DataTesseramento = db.Column(db.Date, unique=False, nullable=False)
    Nome = db.Column(db.String(255), unique=False, nullable=False)
    Cognome = db.Column(db.String(255), unique=False, nullable=False)
    Email = db.Column(db.String(255), unique=False, nullable=False)
    Admin = db.Column(db.Boolean(), unique=False, nullable=False)
    Password = db.Column(db.String(), unique=False, nullable=False)
    CodiceFiscale = db.Column(db.String(16), unique=False, nullable=False)
    Indirizzo = db.Column(db.String(255), unique=False, nullable=False)
    Cap = db.Column(db.String(10), unique=False, nullable=False)
    NumeroTelefono = db.Column(db.String(), unique=False, nullable=False)
    IdTessera = db.Column(db.Integer, db.ForeignKey("Tessera.IdTessera"), unique=True, nullable=False)

    tessere = db.relationship("TesseraModel", backref='Consumatore')


event.listen(ConsumatoreModel, 'before_insert', generazione_stringa_unique)
