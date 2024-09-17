from db import db

class TipoPuntoVenditaModel(db.Model):
    __tablename__ = "TipoPuntoVendita"

    IdTipoPuntoVendita = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(255), unique=True, nullable=False)
    Descrizione = db.Column(db.Text, unique=False, nullable=True)

    puntiVendita = db.relationship('PuntoVenditaModel', backref='TipoPuntoVendita', lazy='dynamic')
