from db import db

class PremioModel(db.Model):
    __tablename__ = "Premio"

    IdPremio = db.Column(db.Integer, primary_key=True)
    Tipologia = db.Column(db.String(255), unique=False, nullable=False)
    Descrizione = db.Column(db.String(255), unique=False, nullable=False)
    Immagine = db.Column(db.String(255), unique=False, nullable=True)
    Url = db.Column(db.String(255), unique=True, nullable=True)
    Soglia = db.Column(db.Integer, unique=False, nullable=True)
    CodicePremio = db.Column(db.Integer, unique=True, nullable=False)
    IdCampagna = db.Column(db.Integer, db.ForeignKey("Campagna.IdCampagna"), unique=False, nullable=False)

    campagne = db.relationship("CampagnaModel", backref='Premio')
