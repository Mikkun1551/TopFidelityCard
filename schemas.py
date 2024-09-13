from marshmallow import Schema, fields


class SchemaAzienda(Schema):
    id_azienda = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    regione = fields.Str(required=True)
    citta = fields.Str(required=True)
    id_tipo_azienda = fields.Int(required=True)
    eliminato = fields.Bool(dump_only=True)

class UpdateAziendaSchema(Schema):
    nome = fields.Str()
    regione = fields.Str()
    citta = fields.Str()
    id_tipo_azienda = fields.Int()


class SchemaTipoAzienda(Schema):
    id_tipo_azienda = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descrizione = fields.Str(required=True)

class UpdateTipoAziendaSchema(Schema):
    nome = fields.Str()
    descrizione = fields.Str()
