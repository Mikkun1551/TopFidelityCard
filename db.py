# PLACEHOLDER DATABASE
id_aziende = 0
id_tipo_aziende = 0


def give_id(type_op):
    """
    Funzione per assegnare id
    :param type_op: Stringa che specifica quale id serve
    :return: Restituisce l'id autoincrementato specifico
    """
    if type_op == 'azienda':
        global id_aziende
        id_aziende += 1
        return id_aziende
    elif type_op == 't_azienda':
        global id_tipo_aziende
        id_tipo_aziende += 1
        return id_tipo_aziende


# La tabella 'azienda' contiene informazioni sulle aziende registrate nel sistema.
aziende = []
# La tabella 'tipoAzienda' contiene informazioni sui tipi di azienda disponibili.
tipi_azienda = []
