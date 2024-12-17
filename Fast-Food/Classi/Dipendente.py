import json
from Gestori.GestoreJSON import GestoreJSON

class Dipendente:
    def __init__(self, nome, cognome, data_di_nascita, telefono, email, username, password):
        self.nome = nome
        self.cognome = cognome
        self.data_di_nascita = data_di_nascita
        self.telefono = telefono
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def accedi(username, password):
        try:
            with open("Dipendenti.json", "r") as file:
                dati_utenti = json.load(file)

            for dipendente in dati_utenti:
                if dipendente["username"] == username and dipendente["password"] == password:
                    return dipendente

            return False
        except FileNotFoundError:
            raise FileNotFoundError("Il file Dipendenti.json non è stato trovato!")
        except json.JSONDecodeError:
            raise ValueError("Errore nella lettura del file Dipendenti.json!")

    @staticmethod
    def visualizza_lista_ordini_clienti():
        from Gestori.GestoreJSON import GestoreJSON

        gestore = GestoreJSON()
        ordini = gestore.leggi_ordini()

        print("\n--- Lista Ordini Clienti ---")
        for ordine in ordini:
            print(f"Codice Ordine: {ordine['codice_ordine']}")
            print(f"Data: {ordine['data']}")
            print(f"Stato: {ordine['stato_ordine']}")
            print("Prodotti:")
            for prodotto in ordine["prodotti"]:
                print(f"  - {prodotto['nome']} ({prodotto['tipo']}): €{prodotto['prezzo']} - {prodotto['punti']} punti")
            print(f"Totale Prezzo: €{ordine['totale']['prezzo']}")
            print(f"Totale Punti: {ordine['totale']['punti']}")
            print("------------------------------")

    @staticmethod
    def conferma_ordine_pronto(codice_ordine):
        from Gestori.GestoreJSON import GestoreJSON

        gestore = GestoreJSON()
        ordini = gestore.leggi_ordini()

        ordini_aggiornati = [ordine for ordine in ordini if ordine["codice_ordine"] != codice_ordine]

        if len(ordini) == len(ordini_aggiornati):
            print(f"Ordine con codice {codice_ordine} non trovato.")
            return

        gestore.salva_ordine_totale(ordini_aggiornati)
        print(f"Ordine con codice {codice_ordine} confermato e rimosso.")


    def salva_ordine_totale(self, ordini):
        try:
            with open(self.ordini_file, "w") as file:
                json.dump(ordini, file, indent=4)
            print("Lista ordini aggiornata con successo.")
        except IOError as e:
            print(f"Errore durante il salvataggio della lista ordini: {e}")

    @staticmethod
    def visualizza_scorte_magazzino():
        gestore = GestoreJSON()
        magazzino = gestore.load_magazzino()

        print("\n--- Scorte Magazzino ---")
        for categoria, prodotti in magazzino.items():
            print(f"\nCategoria: {categoria}")
            for prodotto in prodotti:
                print(f"  - {prodotto['nome']}: Quantità {prodotto['quantita']}, Prezzo €{prodotto['prezzo']}")

    @staticmethod
    def aggiungi_scorte():
        gestore = GestoreJSON()
        magazzino = gestore.load_magazzino()
        aggiornato = False

        for categoria, prodotti in magazzino.items():
            for prodotto in prodotti:
                if prodotto["quantita'"] <= 10:
                    print(f"Il prodotto '{prodotto['nome']}' è stato rifornito a 100 unità.")
                    prodotto["quantita'"] = 100
                    aggiornato = True

        if aggiornato:
            gestore.save_magazzino(magazzino)
            print("Scorte aggiornate con successo.")
        else:
            print("Nessun prodotto necessita di rifornimento.")
