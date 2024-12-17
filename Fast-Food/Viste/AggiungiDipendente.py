from PySide6 import QtCore, QtWidgets, QtGui
from Gestori.GestoreJSON import GestoreJSON


class AggiungiDipendente(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Dipendente")
        self.setGeometry(200, 200, 400, 300)
        self.gestore_json = GestoreJSON()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Aggiungere nuovi dettagli ai dipendenti
        self.nome_edit = QtWidgets.QLineEdit(self)
        self.cognome_edit = QtWidgets.QLineEdit(self)
        self.data_di_nascita_edit = QtWidgets.QLineEdit(self)
        self.telefono_edit = QtWidgets.QLineEdit(self)
        self.email_edit = QtWidgets.QLineEdit(self)
        self.username_edit = QtWidgets.QLineEdit(self)
        self.password_edit = QtWidgets.QLineEdit(self)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Nome:", self.nome_edit)
        form_layout.addRow("Cognome:", self.cognome_edit)
        form_layout.addRow("Data di Nascita:", self.data_di_nascita_edit)
        form_layout.addRow("Telefono:", self.telefono_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Password:", self.password_edit)

        layout.addLayout(form_layout)

        # Bottone per confermare o cancellare l'ordine
        self.add_button = QtWidgets.QPushButton("Aggiungi", self)
        self.cancel_button = QtWidgets.QPushButton("Annulla", self)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.add_button.clicked.connect(self.add_dipendente)
        self.cancel_button.clicked.connect(self.reject)

    def add_dipendente(self):
        # Raccoglie i dati e controlla se sono validi
        nome = self.nome_edit.text().strip()
        cognome = self.cognome_edit.text().strip()
        data_di_nascita = self.data_di_nascita_edit.text().strip()
        telefono = self.telefono_edit.text().strip()
        email = self.email_edit.text().strip()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        if not all([nome, cognome, data_di_nascita, telefono, email, username, password]):
            QtWidgets.QMessageBox.warning(self, "Errore", "Tutti i campi sono obbligatori.")
            return

        if not self.gestore_json.is_valid_email(email):
            QtWidgets.QMessageBox.warning(self, "Errore", "Email non valida.")
            return

        if not self.gestore_json.is_valid_phone_number(telefono):
            QtWidgets.QMessageBox.warning(self, "Errore", "Numero di telefono non valido.")
            return

        if not self.gestore_json.is_unique("dipendenti", {"email": email}):
            QtWidgets.QMessageBox.warning(self, "Errore", "Email già in uso.")
            return

        # Aggiungi dipendente a Json
        nuovo_dipendente = {
            "nome": nome,
            "cognome": cognome,
            "data_di_nascita": data_di_nascita,
            "telefono": telefono,
            "email": email,
            "username": username,
            "password": password
        }
        self.gestore_json.aggiungi_dipendente(nuovo_dipendente)

        QtWidgets.QMessageBox.information(self, "Successo", "Dipendente aggiunto con successo!")
        self.accept()