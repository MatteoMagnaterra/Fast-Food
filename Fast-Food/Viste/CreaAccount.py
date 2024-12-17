import sys
from PySide6 import QtCore, QtWidgets
from Gestori import GestoreJSON, GestoreUtente
import random
import string


class CreaAccount(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Registrati")
        self.setFixedSize(600, 400)
        self.init_ui()

    def init_ui(self):

        self.gestore_json = GestoreJSON.GestoreJSON() # Crea una istanza del gestore JSON
        self.gestore_utente = GestoreUtente.GestoreUtente(self.gestore_json)  # Crea una istanza del gestore utenti

        # Layout principale
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Registrati")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Layout del form
        form_layout = QtWidgets.QGridLayout()

        # Checkbox Cliente e Amministratore
        self.client_checkbox = QtWidgets.QCheckBox("Cliente")
        self.admin_checkbox = QtWidgets.QCheckBox("Amministratore")

        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addWidget(self.client_checkbox)
        checkbox_layout.addWidget(self.admin_checkbox)
        form_layout.addLayout(checkbox_layout, 0, 0, 1, 2)

        # Collegamento delle checkbox
        self.client_checkbox.toggled.connect(self.on_client_checkbox_toggled)
        self.admin_checkbox.toggled.connect(self.on_admin_checkbox_toggled)

        # Campi di input
        self.name_input = self.create_input_field("Nome:")
        self.surname_input = self.create_input_field("Cognome:")
        self.email_input = self.create_input_field("Email:")
        self.password_input = self.create_input_field("Password:", echo_mode=True)
        self.phone_input = self.create_input_field("Telefono:")
        self.username_input = self.create_input_field("Username:")
        self.code_input = self.create_input_field("Codice:", hint="solo se amministratore", read_only=True)

        # Aggiunta dei campi al layout
        form_layout.addWidget(QtWidgets.QLabel("Nome:"), 1, 0)
        form_layout.addWidget(self.name_input, 1, 1)

        form_layout.addWidget(QtWidgets.QLabel("Cognome:"), 2, 0)
        form_layout.addWidget(self.surname_input, 2, 1)

        form_layout.addWidget(QtWidgets.QLabel("Email:"), 3, 0)
        form_layout.addWidget(self.email_input, 3, 1)

        form_layout.addWidget(QtWidgets.QLabel("Password:"), 4, 0)
        form_layout.addWidget(self.password_input, 4, 1)

        form_layout.addWidget(QtWidgets.QLabel("Telefono:"), 5, 0)
        form_layout.addWidget(self.phone_input, 5, 1)

        form_layout.addWidget(QtWidgets.QLabel("Username:"), 6, 0)
        form_layout.addWidget(self.username_input, 6, 1)

        form_layout.addWidget(QtWidgets.QLabel("Codice:"), 7, 0)
        form_layout.addWidget(self.code_input, 7, 1)

        main_layout.addLayout(form_layout)

        # Pulsante di conferma
        confirm_button = QtWidgets.QPushButton("Conferma")
        confirm_button.setStyleSheet("font-size: 16px;")
        confirm_button.clicked.connect(self.submit_form)

        main_layout.addWidget(confirm_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    def create_input_field(self, label, echo_mode=False, hint=None, read_only=False):
        input_field = QtWidgets.QLineEdit()
        if echo_mode:
            input_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        if hint:
            input_field.setPlaceholderText(hint)
        if read_only:
            input_field.setReadOnly(True)
        return input_field

    def on_client_checkbox_toggled(self):
         #Comportamento quando viene selezionato/deselezionato Cliente
        if self.client_checkbox.isChecked():
            self.admin_checkbox.setChecked(False)
            self.code_input.clear()

    def on_admin_checkbox_toggled(self):
        '''Comportamento quando viene selezionato-deselezionato Amministratore'''
        if self.admin_checkbox.isChecked():
            self.client_checkbox.setChecked(False)
            self.generate_code()

    def generate_code(self):
        """Genera un codice casuale per l'amministratore"""
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        self.code_input.setText(code)

    def submit_form(self):
        #Metodo che gestisce il click sul pulsante di conferma e salva i dati nei file JSON.
        nome = self.name_input.text()
        cognome = self.surname_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        telefono = self.phone_input.text()
        username = self.username_input.text()
        codice = self.code_input.text()
        ruolo = "Cliente" if self.client_checkbox.isChecked() else "Amministratore" if self.admin_checkbox.isChecked() else None

        # Chiamata al metodo della classe GestoreUtente
        errore = self.gestore_utente.valida_e_aggiungi_utente(nome, cognome, email, password, telefono, username,
                                                              codice, ruolo)

        if errore:
            QtWidgets.QMessageBox.critical(self, "Errore", errore)
        else:
            QtWidgets.QMessageBox.information(self, "Successo", f"{ruolo} registrato con successo!")
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CreaAccount()
    window.show()
    sys.exit(app.exec())
