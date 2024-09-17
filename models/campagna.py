from db import db

class CampagnaModel(db.Model):
    __tablename__ = "Campagna"

    IdCampagna = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(255), unique=True, nullable=False)
    DataInizio = db.Column(db.Date, unique=False, nullable=False)
    DataFine = db.Column(db.Date, unique=False, nullable=False)
    ConversionePuntiEuro = db.Column(db.Integer, unique=False, nullable=False)
    IdAzienda = db.Column(db.Integer, db.ForeignKey("Azienda.IdAzienda"), unique=False, nullable=False)

    aziende = db.relationship("AziendaModel", backref='Campagna')
