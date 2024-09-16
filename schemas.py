from marshmallow import Schema, fields


class PlainAziendaSchema(Schema):
    IdAzienda = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    Regione = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    P_IVA = fields.Str(required=True)

# class PlainTipoAziendaSchema(Schema):
#     IdTipoAzienda = fields.Int(dump_only=True)
#     Categoria = fields.Str(required=True)
#     Descrizione = fields.Str()
class TipoAziendaSchema(Schema):
    IdTipoAzienda = fields.Int(dump_only=True)
    Categoria = fields.Str(required=True)
    Descrizione = fields.Str()



class UpdateAziendaSchema(Schema):
    Nome = fields.Str()
    Regione = fields.Str()
    Citta = fields.Str()
    Cap = fields.Str()
    P_IVA = fields.Str()
    IdTipoAzienda = fields.Int()

class UpdateTipoAziendaSchema(Schema):
    Categoria = fields.Str()
    Descrizione = fields.Str()



class AziendaSchema(PlainAziendaSchema):
    IdTipoAzienda = fields.Int(required=True, load_only=True)
    # tipoAzienda = fields.Nested(PlainTipoAziendaSchema(), dump_only=True)
    tipoAzienda = fields.Nested(TipoAziendaSchema(), dump_only=True)

# class TipoAziendaSchema(PlainTipoAziendaSchema):
#    aziende = fields.List(fields.Nested(PlainAziendaSchema()), dump_only=True)
