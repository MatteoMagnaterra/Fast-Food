class Ordine:
    def __init__(self, data, codice, stato="In Esecuzione", prodotti=None):
        self.data = data
        self.codice = codice
        self.stato = stato
        self.prodotti = prodotti if prodotti else []