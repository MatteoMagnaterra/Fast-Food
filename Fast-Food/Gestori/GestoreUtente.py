class GestoreUtente:
    def __init__(self, gestore_json):
        self.gestore_json = gestore_json

    def valida_e_aggiungi_utente(self, nome, cognome, email, password, telefono, username, codice, ruolo):
        """
        Metodo che verifica la validità dei dati utente e li aggiunge nei file JSON se tutto è corretto.
        Restituisce un messaggio di errore o None se tutto è valido.
        """
        # Verifica che tutti i campi obbligatori siano compilati
        if not nome or not cognome or not email or not password or not telefono or not username:
            return "Tutti i campi obbligatori devono essere compilati."

        # Verifica se è stato selezionato Cliente o Amministratore
        if ruolo is None:
            return "Selezionare un ruolo: Cliente o Amministratore."

        # Verifica la validità del numero di telefono (deve contenere solo 10 cifre)
        if not self.gestore_json.is_valid_phone_number(telefono):
            return "Il numero di telefono deve contenere solo 10 cifre."

        # Verifica la validità dell'email (deve contenere una '@')
        if not self.gestore_json.is_valid_email(email):
            return "L'email deve contenere un '@'."

        # Creazione dell'utente
        utente = {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "password": password,
            "telefono": telefono,
            "username": username,
            "ruolo": ruolo
        }

        # Aggiunta dell'utente al file appropriato
        if ruolo == "Cliente":
            self.gestore_json.aggiungi_cliente(utente)
        elif ruolo == "Amministratore":
            utente["codice"] = codice
            self.gestore_json.aggiungi_amministratore(utente)

        return None  # Se tutto è valido, ritorna None
