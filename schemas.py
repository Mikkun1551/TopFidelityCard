from marshmallow import Schema, fields


class SchemaAzienda(Schema):
    id_azienda = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    regione = fields.Str(required=True)
    citta = fields.Str(required=True)
    cap = fields.Str(required=True)
    par_iva = fields.Str(required=True)
    id_tipo_azienda = fields.Int(required=True)

class UpdateAziendaSchema(Schema):
    nome = fields.Str()
    regione = fields.Str()
    citta = fields.Str()
    cap = fields.Str()
    par_iva = fields.Str()
    id_tipo_azienda = fields.Int()


class SchemaTipoAzienda(Schema):
    id_tipo_azienda = fields.Int(dump_only=True)
    categoria = fields.Str(required=True)
    descrizione = fields.Str()

class UpdateTipoAziendaSchema(Schema):
    nome = fields.Str()
    descrizione = fields.Str()
