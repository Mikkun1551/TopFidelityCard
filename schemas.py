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

class TipoPuntoVenditaSchema(Schema):
    IdTipoPuntoVendita = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    Descrizione = fields.Str()

class PlainCampagnaSchema(Schema):
    IdCampagna = fields.Int(dump_only=True)
    Nome = fields.Str(required=True)
    DataInizio = fields.Date(required=True)
    DataFine = fields.Date(required=True)
    ConversionePuntiEuro = fields.Int(required=True)

class PlainPremioSchema(Schema):
    IdPremio = fields.Int(dump_only=True)
    Tipologia = fields.Str(required=True)
    Descrizione = fields.Str(required=True)
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int(required=True)

class PlainTesseraSchema(Schema):
    IdTessera = fields.Int(dump_only=True)
    CodiceTessera = fields.Str(required=True)
    DataCreazione = fields.Date(required=True)
    DataScadenza = fields.Date(required=True)



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

class UpdateCampagnaSchema(Schema):
    Nome = fields.Str()
    DataInizio = fields.Date()
    DataFine = fields.Date()
    ConversionePuntiEuro = fields.Int()
    IdAzienda = fields.Int()

class UpdatePremioSchema(Schema):
    Tipologia = fields.Str()
    Descrizione = fields.Str()
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int()
    IdCampagna = fields.Int()

class UpdateTesseraSchema(Schema):
    CodiceTessera = fields.Str()
    DataCreazione = fields.Date()
    DataScadenza = fields.Date()
    IdPuntoVendita = fields.Int()



# Schema a parte per le foreign key (questione di caricamento nel db)
class AziendaSchema(PlainAziendaSchema):
    IdTipoAzienda = fields.Int(required=True)
    tipoAzienda = fields.Nested(TipoAziendaSchema(), dump_only=True)

class PuntoVenditaSchema(PlainPuntoVenditaSchema):
    IdTipoPuntoVendita = fields.Int(required=True)
    tipoPuntoVendita = fields.Nested(TipoPuntoVenditaSchema(), dump_only=True)
    IdAzienda = fields.Int(required=True)
    azienda = fields.Nested(AziendaSchema(), dump_only=True)

class CampagnaSchema(PlainCampagnaSchema):
    IdAzienda = fields.Int(required=True)
    azienda = fields.Nested(AziendaSchema(), dump_only=True)

class PremioSchema(PlainPremioSchema):
    IdCampagna = fields.Int(required=True)
    campagna = fields.Nested(CampagnaSchema(), dump_only=True)

class TesseraSchema(PlainTesseraSchema):
    IdPuntoVendita = fields.Int(required=True)
    puntoVendita = fields.Nested(PuntoVenditaSchema(), dump_only=True)
