from db import db

class PuntoVenditaModel(db.Model):
    __tablename__ = "PuntoVendita"

    IdPuntoVendita = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(255), unique=True, nullable=False)
    Indirizzo = db.Column(db.String(255), unique=False, nullable=False)
    Citta  = db.Column("Città", db.String(100), unique=False, nullable=False)
    Cap = db.Column(db.String(10), unique=False, nullable=False)
    IdTipoPuntoVendita = db.Column(db.Integer, db.ForeignKey("TipoPuntoVendita.IdTipoPuntoVendita"), unique=False, nullable=False)
    IdAzienda = db.Column(db.Integer, db.ForeignKey("Azienda.IdAzienda"), unique=False, nullable=False)

    tipiPuntoVendita = db.relationship("TipoPuntoVenditaModel", backref='PuntoVendita')
    aziende = db.relationship("AziendaModel", backref='PuntoVendita')
