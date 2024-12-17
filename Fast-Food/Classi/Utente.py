from abc import ABC, abstractmethod

class Utente(ABC):
    def __init__(self, nome, cognome, email, password, telefono, username):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.telefono = telefono
        self.username = username

    @abstractmethod
    def accedi(self, username, password):
        """Metodo per autenticare l'utente."""
        pass

    @abstractmethod
    def modifica_account(self, utente):
        """Metodo per modificare i dettagli dell'account."""
        pass

    @abstractmethod
    def visualizza_account(self):
        """Metodo per visualizzare i dettagli dell'account."""
        pass

    @abstractmethod
    def elimina_account(self):
        """Metodo per rimuovere l'account."""
        pass

    @abstractmethod
    def filtra_prodotto(self):
        pass

    @abstractmethod
    def recupera_password(self):
        pass

    @abstractmethod
    def visualizza_prodotti(self):
        pass
