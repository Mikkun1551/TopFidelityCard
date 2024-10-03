from marshmallow import Schema, fields
from bson import ObjectId


# Classe per la conversione ObjectId
class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)  # Conversione ObjectId in stringa per la serializazione

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)  # Conversione stringa in ObjectId per la deserializazione
        except Exception:
            raise ValueError("ObjectId invalido")


# Schema base delle tabelle
class PlainAziendaSchema(Schema):
    IdAzienda = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Regione = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    P_IVA = fields.Str(required=True)

class TipoAziendaSchema(Schema):
    IdTipoAzienda = ObjectIdField(dump_only=True)
    Categoria = fields.Str(required=True)
    Descrizione = fields.Str()

class PlainPuntoVenditaSchema(Schema):
    IdPuntoVendita = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)

class TipoPuntoVenditaSchema(Schema):
    IdTipoPuntoVendita = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Descrizione = fields.Str()

class PlainCampagnaSchema(Schema):
    IdCampagna = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    DataInizio = fields.Date(required=True)
    DataFine = fields.Date(required=True)
    ConversionePuntiEuro = fields.Int(required=True)

class PlainPremioSchema(Schema):
    IdPremio = ObjectIdField(dump_only=True)
    Tipologia = fields.Str(required=True)
    Descrizione = fields.Str(required=True)
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int(required=True)

class PlainTesseraSchema(Schema):
    IdTessera = ObjectIdField(dump_only=True)
    CodiceTessera = fields.Str(required=True)
    DataCreazione = fields.Date(required=True)
    DataScadenza = fields.Date(required=True)

class PlainConsumatoreSchema(Schema):
    IdConsumatore = ObjectIdField(dump_only=True)
    DataTesseramento = fields.Date(required=True)
    Nome = fields.Str(required=True)
    Cognome = fields.Str(required=True)
    Email = fields.Str(required=True)
    Admin = fields.Bool(required=True)
    Password = fields.Str(required=True)
    CodiceFiscale = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Cap = fields.Str(required=True)
    NumeroTelefono = fields.Str(required=True)

class PlainAcquistoSchema(Schema):
    IdAcquisto = ObjectIdField(dump_only=True)
    DataAcquisto = fields.Date(required=True)
    PuntiAcquisiti = fields.Int(required=True)



# Schema per gli update
class UpdateAziendaSchema(Schema):
    Nome = fields.Str()
    Regione = fields.Str()
    Citta = fields.Str()
    Cap = fields.Str()
    P_IVA = fields.Str()
    IdTipoAzienda = ObjectIdField()

class UpdateTipoAziendaSchema(Schema):
    Categoria = fields.Str()
    Descrizione = fields.Str()

class UpdatePuntoVenditaSchema(Schema):
    Nome = fields.Str()
    Indirizzo = fields.Str()
    Citta = fields.Str()
    Cap = fields.Str()
    IdTipoPuntoVendita = ObjectIdField()
    IdAzienda = ObjectIdField()

class UpdateTipoPuntoVenditaSchema(Schema):
    Nome = fields.Str()
    Descrizione = fields.Str()

class UpdateCampagnaSchema(Schema):
    Nome = fields.Str()
    DataInizio = fields.Date()
    DataFine = fields.Date()
    ConversionePuntiEuro = fields.Int()
    IdAzienda = ObjectIdField()

class UpdatePremioSchema(Schema):
    Tipologia = fields.Str()
    Descrizione = fields.Str()
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int()
    IdCampagna = ObjectIdField()

class UpdateTesseraSchema(Schema):
    CodiceTessera = fields.Str()
    DataCreazione = fields.Date()
    DataScadenza = fields.Date()
    IdPuntoVendita = ObjectIdField()

class UpdateConsumatoreSchema(Schema):
    DataTesseramento = fields.Date()
    Nome = fields.Str()
    Cognome = fields.Str()
    Email = fields.Str()
    Admin = fields.Bool()
    Password = fields.Str()
    CodiceFiscale = fields.Str()
    Indirizzo = fields.Str()
    Cap = fields.Str()
    NumeroTelefono = fields.Str()
    IdTessera = ObjectIdField()

class UpdateAcquistoSchema(Schema):
    DataAcquisto = fields.Date()
    PuntiAcquisiti = fields.Int()
    IdConsumatore = ObjectIdField()



# Schema a parte per le foreign key
class AziendaSchema(PlainAziendaSchema):
    IdTipoAzienda = ObjectIdField(required=True)
    tipoAzienda = fields.Nested(TipoAziendaSchema(), dump_only=True)

class PuntoVenditaSchema(PlainPuntoVenditaSchema):
    IdTipoPuntoVendita = ObjectIdField(required=True)
    tipoPuntoVendita = fields.Nested(TipoPuntoVenditaSchema(), dump_only=True)
    IdAzienda = ObjectIdField(required=True)
    azienda = fields.Nested(AziendaSchema(), dump_only=True)

class CampagnaSchema(PlainCampagnaSchema):
    IdAzienda = ObjectIdField(required=True)
    azienda = fields.Nested(AziendaSchema(), dump_only=True)

class PremioSchema(PlainPremioSchema):
    IdCampagna = ObjectIdField(required=True)
    campagna = fields.Nested(CampagnaSchema(), dump_only=True)

class TesseraSchema(PlainTesseraSchema):
    IdPuntoVendita = ObjectIdField(required=True)
    puntoVendita = fields.Nested(PuntoVenditaSchema(), dump_only=True)

class ConsumatoreSchema(PlainConsumatoreSchema):
    IdTessera = ObjectIdField(required=True)
    tessera = fields.Nested(TesseraSchema(), dump_only=True)

class AcquistoSchema(PlainAcquistoSchema):
    IdConsumatore = ObjectIdField(required=True)
    consumatore = fields.Nested(ConsumatoreSchema(), dump_only=True)
