from db import db

class TipoAziendaModel(db.Model):
    __tablename__ = "TipoAzienda"

    IdTipoAzienda = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(255), unique=True, nullable=False)
    Descrizione = db.Column(db.Text, unique=False, nullable=True)

    aziende = db.relationship('AziendaModel', backref='TipoAzienda', lazy='dynamic')
