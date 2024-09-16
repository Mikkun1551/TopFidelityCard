from marshmallow import Schema, fields


class PlainAziendaSchema(Schema):
    idAzienda = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    regione = fields.Str(required=True)
    citta = fields.Str(required=True)
    cap = fields.Str(required=True)
    piva = fields.Str(required=True)

class PlainTipoAziendaSchema(Schema):
    idTipoAzienda = fields.Int(dump_only=True)
    categoria = fields.Str(required=True)
    descrizione = fields.Str()



class UpdateAziendaSchema(Schema):
    nome = fields.Str()
    regione = fields.Str()
    citta = fields.Str()
    cap = fields.Str()
    piva = fields.Str()
    idTipoAzienda = fields.Int()

class UpdateTipoAziendaSchema(Schema):
    categoria = fields.Str()
    descrizione = fields.Str()



class AziendaSchema(PlainAziendaSchema):
    idTipoAzienda = fields.Int(required=True, load_only=True)
    tipoAzienda = fields.Nested(PlainTipoAziendaSchema(), dump_only=True)

class TipoAziendaSchema(PlainTipoAziendaSchema):
    aziende = fields.List(fields.Nested(PlainAziendaSchema()), dump_only=True)
