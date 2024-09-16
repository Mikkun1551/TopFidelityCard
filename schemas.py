from marshmallow import Schema, fields


class SchemaAzienda(Schema):
    idAzienda = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    regione = fields.Str(required=True)
    citta = fields.Str(required=True)
    cap = fields.Str(required=True)
    piva = fields.Str(required=True)
    idTipoAzienda = fields.Int(required=True)

class UpdateAziendaSchema(Schema):
    nome = fields.Str()
    regione = fields.Str()
    citta = fields.Str()
    cap = fields.Str()
    piva = fields.Str()
    idTipoAzienda = fields.Int()


class SchemaTipoAzienda(Schema):
    idTipoAzienda = fields.Int(dump_only=True)
    categoria = fields.Str(required=True)
    descrizione = fields.Str()

class UpdateTipoAziendaSchema(Schema):
    categoria = fields.Str()
    descrizione = fields.Str()
