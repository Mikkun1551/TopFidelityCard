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
    Eliminato = fields.Bool(dump_only=True)

class TipoAziendaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Categoria = fields.Str(required=True)
    Descrizione = fields.Str()
    Eliminato = fields.Bool(dump_only=True)

class PlainPuntoVenditaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Indirizzo = fields.Str(required=True)
    Citta = fields.Str(required=True)
    Cap = fields.Str(required=True)
    Eliminato = fields.Bool(dump_only=True)

class TipoPuntoVenditaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    Descrizione = fields.Str()
    Eliminato = fields.Bool(dump_only=True)

class PlainCampagnaSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Nome = fields.Str(required=True)
    DataInizio = fields.DateTime(required=True)
    DataFine = fields.DateTime(required=True)
    ConversionePuntiEuro = fields.Int(required=True)
    Eliminato = fields.Bool(dump_only=True)

class PlainPremioSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    Tipologia = fields.Str(required=True)
    Descrizione = fields.Str(required=True)
    Immagine = fields.Str()
    Url = fields.Str()
    Soglia = fields.Int()
    CodicePremio = fields.Int(required=True)
    Eliminato = fields.Bool(dump_only=True)

class PlainTesseraSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    CodiceTessera = fields.Str(required=True)
    DataCreazione = fields.DateTime(required=True)
    DataScadenza = fields.DateTime(required=True)
    Eliminato = fields.Bool(dump_only=True)

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
    Eliminato = fields.Bool(dump_only=True)

class PlainAcquistoSchema(Schema):
    _id = ObjectIdField(dump_only=True)
    DataAcquisto = fields.DateTime(required=True)
    PuntiAcquisiti = fields.Int(required=True)
    Eliminato = fields.Bool(dump_only=True)


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


# Schema per le delete
class DeleteAziendaSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteTipoAziendaSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeletePuntoVenditaSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteTipoPuntoVenditaSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteCampagnaSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeletePremioSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteTesseraSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteConsumatoreSchema(Schema):
    Eliminato = fields.Bool(required=True)

class DeleteAcquistoSchema(Schema):
    Eliminato = fields.Bool(required=True)


# Schema per le "foreign key"
class AziendaSchema(PlainAziendaSchema):
    IdTipoAzienda = ObjectIdField(required=True)

class PuntoVenditaSchema(PlainPuntoVenditaSchema):
    IdTipoPuntoVendita = ObjectIdField(required=True)
    IdAzienda = ObjectIdField(required=True)

class CampagnaSchema(PlainCampagnaSchema):
    IdAzienda = ObjectIdField(required=True)

class PremioSchema(PlainPremioSchema):
    IdCampagna = ObjectIdField(required=True)

class TesseraSchema(PlainTesseraSchema):
    IdPuntoVendita = ObjectIdField(required=True)

class ConsumatoreSchema(PlainConsumatoreSchema):
    IdTessera = ObjectIdField(required=True)

class AcquistoSchema(PlainAcquistoSchema):
    IdConsumatore = ObjectIdField(required=True)
