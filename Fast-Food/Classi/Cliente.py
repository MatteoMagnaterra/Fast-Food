from Classi.Utente import Utente
from Gestori.GestoreJSON import GestoreJSON
import datetime
import json
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Cliente(Utente):
    def __init__(self, nome, cognome, email, password, telefono, username):
        super().__init__(nome, cognome, email, password, telefono, username)
        self.gestore_json = GestoreJSON()

    @staticmethod
    def accedi(username, password):
        try:
            with open("Utenti.json", "r") as file:
                dati_utenti = json.load(file)

            for cliente in dati_utenti.get("clienti", []):
                if cliente["username"] == username and cliente["password"] == password:
                    return cliente

            return False
        except FileNotFoundError:
            raise FileNotFoundError("Il file Utenti.json non è stato trovato!")
        except json.JSONDecodeError:
            raise ValueError("Errore nella lettura del file Utenti.json!")

    def modifica_account(self, nuovi_dati):
        field_values = {"username": nuovi_dati["username"], "password": nuovi_dati["password"]}
        if self.gestore_json.is_unique("clienti", field_values, current_username=self.username):
            self.gestore_json.modifica_dati("clienti", self.username, nuovi_dati)
            self.nome = nuovi_dati["nome"]
            self.cognome = nuovi_dati["cognome"]
            self.email = nuovi_dati["email"]
            self.password = nuovi_dati["password"]
            self.telefono = nuovi_dati["telefono"]
            self.username = nuovi_dati["username"]
            return True
        else:
            print("Errore: username o codice già in uso. Scegli valori diversi.")
            return False

    def visualizza_account(self):
        try:
            dati_utenti = self.gestore_json.load_data()  # Usa il metodo caricato dai test

            for cliente in dati_utenti.get("clienti", []):
                if cliente["username"] == self.username:
                    return {
                        "nome": cliente["nome"],
                        "cognome": cliente["cognome"],
                        "email": cliente["email"],
                        "password": cliente["password"],
                        "telefono": cliente["telefono"],
                        "username": cliente["username"]
                    }
            print("Cliente non trovato!")
            return None
        except Exception as e:
            print(f"Errore: {e}")
            return None

    def elimina_account(self):
        self.gestore_json.delete_data_cliente(self.username, self.password)
        print("Account amministratore eliminato con successo.")

    def visualizza_prodotti(self, magazzino):
        print("\n--- Prodotti disponibili ---")
        for categoria, prodotti in magazzino.items():
            print(f"\nCategoria: {categoria}")
            for prodotto in prodotti:
                print(f"- {prodotto['nome']}: €{prodotto['prezzo']} ({prodotto['quantita']} disponibili, {prodotto['punti']} punti)")

    def filtra_prodotto(self, magazzino, filtro):
        prodotti_trovati = []
        for categoria, prodotti in magazzino.items():
            for prodotto in prodotti:
                if filtro.lower() in prodotto["nome"].lower() or filtro.lower() in ", ".join(prodotto["ingredienti"]).lower():
                    prodotti_trovati.append({
                        "categoria": categoria,
                        "nome": prodotto["nome"],
                        "prezzo": prodotto["prezzo"],
                        "quantita": prodotto["quantita"]
                    })
        if prodotti_trovati:
            print("\n--- Prodotti filtrati ---")
            for p in prodotti_trovati:
                print(f"Categoria: {p['categoria']}, Nome: {p['nome']}, Prezzo: €{p['prezzo']}, Quantità: {p['quantita']}")
        else:
            print("Nessun prodotto trovato con il filtro fornito.")
        return prodotti_trovati

    def recupera_password(self, email):
        try:
            dati_utenti = self.gestore_json.load_data()

            for cliente in dati_utenti.get("clienti", []):
                if cliente["email"] == email:
                    nuova_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                    cliente["password"] = nuova_password

                    self.gestore_json.salva_dati(dati_utenti)

                    self.invia_email_password(email, nuova_password)
                    print("Una nuova password è stata inviata al tuo indirizzo email.")
                    return True

            print("Email non trovata. Impossibile recuperare la password.")
            return False

        except Exception as e:
            print(f"Errore durante il recupero della password: {e}")
            return False

    def invia_email_password(self, email, nuova_password):
        mittente = "noreply@fastfood.com"
        oggetto = "Recupero Password - Fast Food"
        corpo_email = f"La tua nuova password è: {nuova_password}\nTi consigliamo di cambiarla appena possibile."

        msg = MIMEMultipart()
        msg['From'] = mittente
        msg['To'] = email
        msg['Subject'] = oggetto
        msg.attach(MIMEText(corpo_email, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(mittente, "password_mittente")
            server.send_message(msg)
            server.quit()
            print(f"Email inviata con successo a {email}.")
        except Exception as e:
            print(f"Errore durante l'invio dell'email: {e}")

    def seleziona_prodotti(self, magazzino):
        prodotti_selezionati = []
        while True:
            nome_prodotto = input("\nInserisci il nome del prodotto da aggiungere al ordine (o 'fine' per terminare): ").strip()
            if nome_prodotto.lower() == 'fine':
                break

            prodotto_trovato = self.trova_prodotto(magazzino, nome_prodotto)
            if not prodotto_trovato:
                print("Prodotto non trovato. Riprova.")
                continue

            quantita = int(input(f"Quanti {nome_prodotto} vuoi ordinare? "))
            if quantita > prodotto_trovato["quantita"]:
                print(f"Quantità non disponibile. Disponibili: {prodotto_trovato['quantita']}.")
                continue

            self.aggiungi_prodotto_all_ordine(prodotti_selezionati, prodotto_trovato, quantita)
        return prodotti_selezionati

    def trova_prodotto(self, magazzino, nome_prodotto):
        for categoria, prodotti in magazzino.items():
            for prodotto in prodotti:
                if prodotto["nome"].lower() == nome_prodotto.lower():
                    return prodotto
        return None

    def aggiungi_prodotto_all_ordine(self, ordine, prodotto, quantita):
        ordine.append({
            "nome": prodotto["nome"],
            "prezzo": prodotto["prezzo"],
            "quantita": quantita,
            "punti": prodotto["punti"] * quantita
        })
        prodotto["quantita"] -= quantita
        print(f"{quantita} {prodotto['nome']} aggiunti al ordine.")

    def conferma_ordine(self, ordine, magazzino):
        self.gestore_json.salva_ordine(ordine)
        self.gestore_json.save_magazzino(magazzino)
        print("Ordine confermato con successo!")

    def annulla_ordine(self, ordine, magazzino):
        for item in ordine:
            prodotto = self.trova_prodotto(magazzino, item["nome"])
            if prodotto:
                prodotto["quantita"] += item["quantita"]
        print("Ordine annullato e magazzino ripristinato.")

    def effettua_ordine(self):
        magazzino = self.gestore_json.load_magazzino()
        if not magazzino:
            print("Il magazzino è vuoto o non disponibile.")
            return None

        self.visualizza_prodotti(magazzino)
        prodotti_selezionati = self.seleziona_prodotti(magazzino)

        prezzo_totale = sum(item["prezzo"] * item["quantita"] for item in prodotti_selezionati)
        punti_totali = sum(item["punti"] for item in prodotti_selezionati)

        if not prodotti_selezionati:
            print("Nessun prodotto selezionato. Ordine annullato.")
            return None

        print("\n--- Riepilogo Ordine ---")
        for item in prodotti_selezionati:
            print(f"- {item['nome']} x{item['quantita']}: €{item['prezzo'] * item['quantita']} ({item['punti']} punti)")
        print(f"Totale: €{prezzo_totale}, Punti: {punti_totali}")

        conferma = input("Vuoi confermare l'ordine? (sì/no): ").strip().lower()
        if conferma == 'sì':
            nuovo_ordine = {
                "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "stato_ordine": "In Esecuzione",
                "prodotti": prodotti_selezionati,
                "totale": {
                    "prezzo": prezzo_totale,
                    "punti": punti_totali
                }
            }
            self.conferma_ordine(nuovo_ordine, magazzino)
            return nuovo_ordine
        else:
            self.annulla_ordine(prodotti_selezionati, magazzino)
            return None

    def crea_feedback(self, voto):
        if not 1 <= voto <= 5:
            print("Errore: il voto deve essere compreso tra 1 e 5 stelle.")
            return False
        try:
            self.gestore_json.salva_feedback(voto)
            print(f"Feedback di {voto} stelle salvato con successo.")
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio del feedback: {e}")
            return False