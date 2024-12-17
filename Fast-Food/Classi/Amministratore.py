from Classi.Utente import Utente
from Gestori.GestoreJSON import GestoreJSON
import string
import random


class Amministratore(Utente):
    def __init__(self, nome, cognome, email, password, telefono, username, codice):
        super().__init__(nome, cognome, email, password, telefono, username)
        self.codice = codice
        self.gestore_json = GestoreJSON()

    @staticmethod
    def accedi(username, password, codice):
        gestore_json = GestoreJSON()
        dati_utenti = gestore_json.load_data()

        for admin in dati_utenti.get("amministratori", []):
            if (admin["username"] == username and
                    admin["password"] == password and
                    admin["codice"] == codice):
                # Restituisce tutti i dati dell'amministratore
                return admin

        return None

    def modifica_account(self, nuovi_dati):
        # Verifica l'unicità dei nuovi valori di username e codice
        field_values = {"username": nuovi_dati["username"], "codice": nuovi_dati["codice"]}
        if self.gestore_json.is_unique("amministratori", field_values, current_username=self.username):
            # Aggiorna i dati dell'amministratore se sono unici
            self.gestore_json.modifica_dati("amministratori", self.username, nuovi_dati)
            # Aggiorna anche l'oggetto amministratore corrente
            self.nome = nuovi_dati["nome"]
            self.cognome = nuovi_dati["cognome"]
            self.email = nuovi_dati["email"]
            self.password = nuovi_dati["password"]
            self.telefono = nuovi_dati["telefono"]
            self.username = nuovi_dati["username"]
            self.codice = nuovi_dati["codice"]
            return True
        else:
            print("Errore: username o codice già in uso. Scegli valori diversi.")
            return False

    def visualizza_account(self):
        try:
            dati_utenti = self.gestore_json.load_data()  # Usa il metodo caricato dai test

            for amministratore in dati_utenti.get("amministratori", []):
                if amministratore["username"] == self.username and amministratore["codice"] == self.codice:
                    return {
                        "nome": amministratore["nome"],
                        "cognome": amministratore["cognome"],
                        "email": amministratore["email"],
                        "password": amministratore["password"],
                        "telefono": amministratore["telefono"],
                        "username": amministratore["username"],
                        "codice": amministratore["codice"]
                    }
            print("Amministratore non trovato!")
            return None
        except Exception as e:
            print(f"Errore: {e}")
            return None

    def elimina_account(self):
        """Elimina l'account dell'amministratore usando GestoreJSON."""
        self.gestore_json.delete_data_amministratore(self.username, self.codice)
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

    def aggiungi_dipendente(self, nome, cognome, data_di_nascita, telefono, email, username, password):
        dipendente = {
            "nome": nome,
            "cognome": cognome,
            "data_di_nascita": data_di_nascita,
            "telefono": telefono,
            "email": email,
            "username": username,
            "password": password
        }
        try:
            self.gestore_json.aggiungi_dipendente(dipendente)
            print(f"Dipendente {nome} {cognome} aggiunto con successo.")
        except Exception as e:
            print(f"Errore durante l'aggiunta del dipendente: {e}")

    def modifica_dipendente(self, email_corrente, nuovi_dati):
        try:
            self.gestore_json.modifica_dipendente(email_corrente, nuovi_dati)
            print(f"Dipendente con email {email_corrente} modificato con successo.")
        except ValueError as e:
            print(f"Errore: {e}")
        except Exception as e:
            print(f"Errore inatteso: {e}")

    def elimina_dipendente(self, email):
        try:
            self.gestore_json.elimina_dipendente(email)
            print(f"Dipendente con email {email} eliminato con successo.")
        except ValueError as e:
            print(f"Errore: {e}")
        except Exception as e:
            print(f"Errore inatteso: {e}")

    def aggiungi_prodotto(self, categoria, nome, ingredienti, prezzo, quantita, punti):
        try:
            self.gestore_json.aggiungi_prodotto(categoria, nome, ingredienti, prezzo, quantita, punti)
            print(f"Prodotto '{nome}' aggiunto con successo nella categoria '{categoria}'.")
        except ValueError as e:
            print(f"Errore: {e}")
        except Exception as e:
            print(f"Errore inatteso: {e}")

    def modifica_prodotto(self, categoria, nome_corrente, nuovi_dati):
        try:
            self.gestore_json.modifica_prodotto(categoria, nome_corrente, nuovi_dati)
            print(f"Prodotto '{nome_corrente}' modificato con successo nella categoria '{categoria}'.")
        except ValueError as e:
            print(f"Errore: {e}")
        except Exception as e:
            print(f"Errore inatteso: {e}")

    def elimina_prodotto(self, categoria, nome):
        try:
            self.gestore_json.elimina_prodotto(categoria, nome)
            print(f"Prodotto '{nome}' eliminato con successo dalla categoria '{categoria}'.")
        except ValueError as e:
            print(f"Errore: {e}")
        except Exception as e:
            print(f"Errore inatteso: {e}")

    def visualizza_feedback(self):
        try:
            feedback = self.gestore_json.leggi_feedback()
            if feedback:
                print("\n--- Feedback ricevuti ---")
                for i, entry in enumerate(feedback, start=1):
                    print(f"{i}. {entry['voto']} stelle")
            else:
                print("Nessun feedback disponibile.")
        except Exception as e:
            print(f"Errore durante la visualizzazione dei feedback: {e}")

    def visualizza_dipendenti(self):
        try:
            dipendenti = self.gestore_json.load_dipendenti()
            if dipendenti:
                print("\n--- Elenco Dipendenti ---")
                for i, dipendente in enumerate(dipendenti, start=1):
                    print(f"{i}. {dipendente['nome']} {dipendente['cognome']} - Email: {dipendente['email']} - Telefono: {dipendente['telefono']}")
            else:
                print("Nessun dipendente trovato.")
        except Exception as e:
            print(f"Errore durante la visualizzazione dei dipendenti: {e}")

