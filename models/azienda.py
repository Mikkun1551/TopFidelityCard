from db import db

class AziendaModel(db.Model):
    __tablename__ = "Azienda"

    IdAzienda = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(255), unique=True, nullable=False)
    Regione = db.Column(db.String(100), unique=False, nullable=False)
    Citta  = db.Column("Città", db.String(100), unique=False, nullable=False)
    Cap = db.Column(db.String(10), unique=False, nullable=False)
    P_IVA  = db.Column("P.IVA", db.String(10), unique=True, nullable=False)
    IdTipoAzienda = db.Column(db.Integer, db.ForeignKey("TipoAzienda.IdTipoAzienda"), unique=False, nullable=False)

    tipiAzienda = db.relationship("TipoAziendaModel", backref='Azienda')
