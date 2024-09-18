from db import db

class AcquistoModel(db.Model):
    __tablename__ = "Acquisto"

    IdAcquisto = db.Column(db.Integer, primary_key=True)
    DataAcquisto = db.Column(db.Date, unique=False, nullable=False)
    PuntiAcquisiti = db.Column(db.Integer, unique=False, nullable=False)
    IdConsumatore = db.Column(db.String(12), db.ForeignKey("Consumatore.IdConsumatore"), unique=False, nullable=False)

    consumatori = db.relationship("ConsumatoreModel", backref='Acquisto')
