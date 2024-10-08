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
        except Exception as e:
            return e
            # raise ValueError("ObjectId invalido")


# Schema base delle tabelle
class PlainAziendaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Regione = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    P_IVA = fields.Str(required=True)
    Eliminato = fields.Bool()

class TipoAziendaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Categoria = fields.Str(required=True)
    Descrizione = fields.Str()
    Eliminato = fields.Bool()

class PlainPuntoVenditaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    Eliminato = fields.Bool()

class TipoPuntoVenditaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Descrizione = fields.Str()
    Eliminato = fields.Bool()

class PlainCampagnaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    DataInizio = fields.DateTime(required=True)
    DataFine = fields.DateTime(required=True)
    ConversionePuntiEuro = fields.Int(required=True)
    Eliminato = fields.Bool()

class PlainPremioSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Tipologia = fields.Str(required=True)
    Descrizione = fields.Str(required=True)
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int(required=True)
    Eliminato = fields.Bool()

class PlainTesseraSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    CodiceTessera = fields.Str(required=True)
    DataCreazione = fields.DateTime(required=True)
    DataScadenza = fields.DateTime(required=True)
    Eliminato = fields.Bool()

class PlainConsumatoreSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    DataTesseramento = fields.DateTime(required=True)
    Nome = fields.Str(required=True)
    Cognome = fields.Str(required=True)
    Email = fields.Str(required=True)
    Admin = fields.Bool(required=True)
    Password = fields.Str(required=True)
    CodiceFiscale = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Cap = fields.Str(required=True)
    NumeroTelefono = fields.Str(required=True)
    Eliminato = fields.Bool()

class PlainAcquistoSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    DataAcquisto = fields.DateTime(required=True)
    PuntiAcquisiti = fields.Int(required=True)
    Eliminato = fields.Bool()



class DeleteAcquistoSchema(Schema):
    Eliminato = fields.Bool(required=True)



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
    DataInizio = fields.DateTime()
    DataFine = fields.DateTime()
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
    DataCreazione = fields.DateTime()
    DataScadenza = fields.DateTime()
    IdPuntoVendita = ObjectIdField()

class UpdateConsumatoreSchema(Schema):
    DataTesseramento = fields.DateTime()
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
    DataAcquisto = fields.DateTime()
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
