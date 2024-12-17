class Fattura:
    def __init__(self, codice_ricevuta, data, ora, ordine, totale):
        self.codice_ricevuta = codice_ricevuta
        self.data = data
        self.ora = ora
        self.ordine = ordine
        self.totale = totale

    def get_codice_ricevuta(self):
        return self.codice_ricevuta

    def get_data(self):
        return self.data

    def get_ora(self):
        return self.ora

    def get_ordine(self):
        return self.ordine

    def get_totale(self):
        return self.totale

    def visualizza_ricevuta(self):
        print(f"Codice Ricevuta: {self.get_codice_ricevuta()}")
        print(f"Data: {self.get_data()}")
        print(f"Ora: {self.get_ora()}")
        print(f"Ordine: {self.get_ordine()}")
        print(f"Totale: {self.get_totale()}")