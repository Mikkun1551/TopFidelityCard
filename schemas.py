from marshmallow import Schema, fields


# Schema base delle tabelle
class PlainAziendaSchema(Schema):
    IdAzienda = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    Regione = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    P_IVA = fields.Str(required=True)

class TipoAziendaSchema(Schema):
    IdTipoAzienda = fields.Int(dump_only=True)
    Categoria = fields.Str(required=True)
    Descrizione = fields.Str()

class PlainPuntoVenditaSchema(Schema):
    IdPuntoVendita = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    IdTipoPuntoVendita = fields.Int(required=True)
    IdAzienda = fields.Int(required=True)

class TipoPuntoVenditaSchema(Schema):
    IdTipoPuntoVendita = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    Descrizione = fields.Str()


# Schema per gli update
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

class UpdatePuntoVenditaSchema(Schema):
    Nome = fields.Str()
    Indirizzo = fields.Str()
    Citta = fields.Str()
    Cap = fields.Str()
    IdTipoPuntoVendita = fields.Int()
    IdAzienda = fields.Int()

class UpdateTipoPuntoVenditaSchema(Schema):
    Nome = fields.Str()
    Descrizione = fields.Str()



# Schema a parte per le foreign key (questione di caricamento nel db)
class AziendaSchema(PlainAziendaSchema):
    IdTipoAzienda = fields.Int(required=True, load_only=True)
    tipoAzienda = fields.Nested(TipoAziendaSchema(), dump_only=True)

class PuntoVenditaSchema(PlainPuntoVenditaSchema):
    IdTipoPuntoVendita = fields.Int(required=True, load_only=True)
    tipoPuntoVendita = fields.Nested(TipoPuntoVenditaSchema(), dump_only=True)
