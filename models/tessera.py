from db import db

class TesseraModel(db.Model):
    __tablename__ = "Tessera"

    IdTessera = db.Column(db.Integer, primary_key=True)
    CodiceTessera = db.Column(db.String(50), unique=True, nullable=False)
    DataCreazione = db.Column(db.Date, unique=False, nullable=False)
    DataScadenza = db.Column(db.Date, unique=False, nullable=False)
    IdPuntoVendita = db.Column(db.Integer, db.ForeignKey("PuntoVendita.IdPuntoVendita"), unique=False, nullable=False)

    puntiVendita = db.relationship("PuntoVenditaModel", backref='Tessera')
