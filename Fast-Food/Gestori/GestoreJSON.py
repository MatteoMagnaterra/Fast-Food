import json
import os
from PySide6.QtWidgets import QMessageBox


class GestoreJSON:
    def __init__(self):
        # Percorso del file JSON
        self.utenti_file = "Utenti.json"
        self.dipendenti_file = "Dipendenti.json"
        self.magazzino_file = "Magazzino.json"
        self.feedback_file = "feedback.json"
        self.ordini_file = "Ordini.json"

    def load_data(self):
        #Carica i dati dal file JSON. Se il file non esiste o è vuoto, ritorna una struttura vuota.
        if os.path.exists(self.utenti_file) and os.path.getsize(self.utenti_file) > 0:
            with open(self.utenti_file, "r") as file:
                return json.load(file)
        else:
            return {"clienti": [], "amministratori": []}  # Struttura vuota

    def save_data(self, data):
        #Salva i dati nel file JSON.
        with open(self.utenti_file, "w") as file:
            json.dump(data, file, indent=4)

    def delete_data_amministratore(self, username, codice):
        #Elimina un utente (cliente o amministratore) dal file JSON.
        dati_utenti = self.load_data()

        # Rimuovere l'amministratore con lo username e codice specificato
        amministratori = [
            admin for admin in dati_utenti["amministratori"]
            if not (admin["username"] == username and admin["codice"] == codice)
        ]
        dati_utenti["amministratori"] = amministratori

        # Salvare i dati aggiornati
        self.save_data(dati_utenti)

    def delete_data_cliente(self, username, password):
        """Elimina un cliente dal file JSON."""
        dati_utenti = self.load_data()

        # Rimuovere il cliente con lo username e password specificati
        clienti = [
            cliente for cliente in dati_utenti["clienti"]
            if not (cliente["username"] == username and cliente["password"] == password)
        ]
        dati_utenti["clienti"] = clienti

        # Salvare i dati aggiornati
        self.save_data(dati_utenti)

    def aggiungi_cliente(self, cliente):
        """Aggiungi un nuovo cliente alla sezione 'clienti' nel file JSON."""
        dati_utenti = self.load_data()
        dati_utenti["clienti"].append(cliente)
        self.save_data(dati_utenti)

    def aggiungi_amministratore(self, amministratore):
        """Aggiungi un nuovo amministratore alla sezione 'amministratori' nel file JSON."""
        dati_utenti = self.load_data()
        dati_utenti["amministratori"].append(amministratore)
        self.save_data(dati_utenti)

    def aggiungi_dipendente(self, dipendente):
        # Aggiunge un nuovo dipendente al file Dipendenti.json.
        try:
            dipendenti = self.load_dipendenti()
            dipendenti.append(dipendente)
            self.save_dipendenti(dipendenti)
        except Exception as e:
            print("Errore durante l'aggiunta del dipendente:", str(e))
            raise

    @staticmethod
    def is_valid_phone_number(phone_number):
        """Verifica che il numero di telefono contenga solo 10 cifre."""
        return len(phone_number) == 10 and phone_number.isdigit()  # Controlla che sia lungo 10 e contenga solo numeri

    @staticmethod
    def is_valid_email(email):
        # Rimuove eventuali spazi iniziali o finali
        email = email.strip()
        # Controlla che non ci siano spazi vuoti
        if " " in email:
            return False
        # Verifica la presenza di '@' e '.'
        return '@' in email and '.' in email

    def is_unique(self, user_type, field_values, current_username=None):
        #Verifica se i valori forniti per uno o più campi sono unici per un certo tipo di utente.
        dati_utenti = self.load_data()
        utenti = dati_utenti.get(user_type, [])

        for utente in utenti:
            # Ignora l'attuale utente che si sta modificando
            if current_username and utente.get("username") == current_username:
                continue
            for field, value in field_values.items():
                if utente.get(field) == value:
                    return False
        return True

    def modifica_dati(self, user_type, identificatore, nuovi_dati):
        #Modifica i dati di un utente (es: amministratori, clienti) nel file JSON.
        dati_utenti = self.load_data()
        utenti = dati_utenti.get(user_type, [])

        for utente in utenti:
            if utente["username"] == identificatore:  # Puoi cambiare "email" con il campo chiave del record
                utente.update(nuovi_dati)
                break
        else:
            raise ValueError(f"{user_type.capitalize()} con identificatore {identificatore} non trovato.")

        self.save_data(dati_utenti)

    def salva_ordine(self, ordine):
        try:
            # Carica gli ordini esistenti
            if os.path.exists(self.ordini_file) and os.path.getsize(self.ordini_file) > 0:
                with open(self.ordini_file, "r") as file:
                    ordini = json.load(file)
            else:
                ordini = []  # Inizia con una lista vuota se il file non esiste

            # Aggiungi il nuovo ordine
            ordini.append(ordine)

            # Salva nel file
            with open(self.ordini_file, "w") as file:
                json.dump(ordini, file, indent=4)

            print("Ordine salvato con successo.")
        except Exception as e:
            print(f"Errore durante il salvataggio dell'ordine: {str(e)}")

    def elimina_dipendente(self, email):
        #Elimina un dipendente dal file Dipendenti.json.
        dipendenti = self.load_dipendenti()

        # Filtra i dipendenti rimuovendo quello con l'email specificata
        dipendenti_filtrati = [d for d in dipendenti if d["email"] != email]

        # Controlla se il dipendente è stato trovato
        if len(dipendenti) == len(dipendenti_filtrati):
            raise ValueError(f"Dipendente con email {email} non trovato.")

        # Salva i dati aggiornati
        self.save_dipendenti(dipendenti_filtrati)
        print(f"Dipendente con email {email} eliminato con successo.")

    def load_dipendenti(self):
        #Carica i dati dei dipendenti dal file JSON.
        if os.path.exists(self.dipendenti_file) and os.path.getsize(self.dipendenti_file) > 0:
            with open(self.dipendenti_file, "r") as file:
                return json.load(file)
        else:
            return []

    def save_dipendenti(self, data):
        try:
            with open(self.dipendenti_file, "w") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print("Errore nel salvataggio dei dati:", str(e))
            raise

    def modifica_dipendente(self, email_corrente, nuovi_dati):

        # Carica i dati dal file JSON dei dipendenti
        dipendenti = self.load_dipendenti()
        # Cerca il dipendente con l'email corrente
        for dipendente in dipendenti:
            if dipendente["email"] == email_corrente:
                # Aggiorna i dati del dipendente
                dipendente.update(nuovi_dati)
                break
        else:
            raise ValueError(f"Dipendente con email {email_corrente} non trovato.")

        # Salva i dati aggiornati nel file Dipendenti.json
        self.save_dipendenti(dipendenti)
        print(f"Dipendente con email {email_corrente} aggiornato con successo.")

    def load_magazzino(self):
        #Carica il magazzino dalla struttura JSON con categorie.
        try:
            with open("Magazzino.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Magazzino.json non trovato.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Errore nella decodifica di Magazzino.json: {e}")
            return {}

    def save_magazzino(self, magazzino):
        try:
            with open(self.magazzino_file, "w") as file:
                json.dump(magazzino, file, indent=4)
            print("Magazzino salvato correttamente.")
        except IOError as e:
            print(f"Errore durante il salvataggio del magazzino: {e}")


    def aggiungi_prodotto(self, categoria, nome, ingredienti, prezzo, quantita, punti):
        #Aggiunge un nuovo prodotto al magazzino.
        magazzino = self.load_magazzino()

        if categoria not in magazzino:
            raise ValueError(f"Categoria '{categoria}' non trovata.")

        # Controlla duplicati
        if any(prodotto["nome"] == nome for prodotto in magazzino[categoria]):
            raise ValueError(f"Un prodotto con il nome '{nome}' esiste già nella categoria '{categoria}'.")

        nuovo_prodotto = {
            "nome": nome,
            "ingredienti": ingredienti,
            "prezzo": prezzo,
            "quantita'": quantita,
            "punti": punti
        }

        magazzino[categoria].append(nuovo_prodotto)
        self.save_magazzino(magazzino)
        print(f"Prodotto '{nome}' aggiunto con successo alla categoria '{categoria}'.")

    def modifica_prodotto(self, categoria, nome_corrente, nuovi_dati):
        magazzino = self.load_magazzino()

        if categoria not in magazzino:
            raise ValueError(f"Categoria '{categoria}' non trovata.")

        for prodotto in magazzino[categoria]:
            if prodotto["nome"] == nome_corrente:
                # Aggiorna solo i campi presenti in nuovi_dati
                prodotto.update({k: v for k, v in nuovi_dati.items() if v is not None})
                self.save_magazzino(magazzino)
                print(f"Prodotto '{nome_corrente}' modificato con successo.")
                return

        raise ValueError(f"Prodotto '{nome_corrente}' non trovato nella categoria '{categoria}'.")

    def elimina_prodotto(self, categoria, nome):
        magazzino = self.load_magazzino()

        if categoria not in magazzino:
            raise ValueError(f"Categoria '{categoria}' non trovata.")

        prodotti_filtrati = [prodotto for prodotto in magazzino[categoria] if prodotto["nome"] != nome]

        if len(prodotti_filtrati) == len(magazzino[categoria]):
            raise ValueError(f"Prodotto '{nome}' non trovato nella categoria '{categoria}'.")

        magazzino[categoria] = prodotti_filtrati
        self.save_magazzino(magazzino)
        print(f"Prodotto '{nome}' eliminato con successo dalla categoria '{categoria}'.")

    def leggi_ordini(self):
        try:
            with open(self.ordini_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(None, "File Non Trovato", f"Il file '{self.ordini_file}' non è stato trovato.")
            return []
        except json.JSONDecodeError:
            QMessageBox.critical(None, "Errore di Lettura", f"Errore nella lettura del file '{self.ordini_file}'.")
            return []

    def salva_ordine_totale(self, ordini):
        """Salva la lista completa degli ordini nel file JSON."""
        try:
            with open(self.ordini_file, "w") as file:
                json.dump(ordini, file, indent=4)
            print("Lista ordini aggiornata con successo.")
        except IOError as e:
            print(f"Errore durante il salvataggio della lista ordini: {e}")

    def reset_quantita_prodotto(self, categoria, nome_prodotto, nuova_quantita):
        """
        Resetta la quantità di un prodotto specifico a un valore fisso.
        :param categoria: Categoria del prodotto (es. "panini", "bevande").
        :param nome_prodotto: Nome del prodotto.
        :param nuova_quantita: La nuova quantità da impostare.
        """
        magazzino = self.load_magazzino()

        if categoria not in magazzino:
            raise ValueError(f"Categoria '{categoria}' non trovata.")

        for prodotto in magazzino[categoria]:
            if prodotto["nome"] == nome_prodotto:
                prodotto["quantita'"] = nuova_quantita
                self.save_magazzino(magazzino)
                return

        raise ValueError(f"Prodotto '{nome_prodotto}' non trovato nella categoria '{categoria}'.")
