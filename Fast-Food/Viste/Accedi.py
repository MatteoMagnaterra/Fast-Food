import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Viste.RecuperaPassword import PasswordRecoveryWindow
from Viste.CreaAccount import CreaAccount
from Viste.HomepageCliente import HomepageCliente
from Viste.HomepageAmministratore import HomepageAmministratore
from Classi.Amministratore import Amministratore
from Classi.Cliente import Cliente
from Classi.Dipendente import Dipendente
from Viste.HomepageDipendente import HomepageDipendente


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food")
        self.setGeometry(300, 250, 600, 500)
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Accedi", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title_label)

        # Form layout inside a group box for better styling
        form_group_box = QtWidgets.QGroupBox()
        form_layout = QtWidgets.QFormLayout(form_group_box)

        # Username e Password
        self.username_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.codice_input = QtWidgets.QLineEdit(self)
        self.codice_input.setPlaceholderText("Codice (solo se Amministratore)")

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Codice:", self.codice_input)
        main_layout.addWidget(form_group_box)

        # Bottoni
        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Accedi", self)
        self.forgot_password_button = QtWidgets.QPushButton("Recupero password", self)
        self.register_button = QtWidgets.QPushButton("Registrati", self)

        # Stile bottoni
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.forgot_password_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.register_button.setStyleSheet("background-color: #f44336; color: white;")

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.forgot_password_button)
        button_layout.addWidget(self.register_button)

        # Posizione bottoni
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        # Collegamenti
        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.show_password_recovery)
        self.register_button.clicked.connect(self.handle_register)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        codice = self.codice_input.text()

        if username and password:
            if codice:
                # Tentativo di login come amministratore
                try:
                    admin = Amministratore(None, None, None, None, None, username, codice)
                    dati_amministratore = admin.accedi(username, password, codice)

                    if dati_amministratore:
                        admin.nome = dati_amministratore["nome"]
                        admin.cognome = dati_amministratore["cognome"]
                        admin.email = dati_amministratore["email"]
                        admin.telefono = dati_amministratore["telefono"]
                        admin.password = dati_amministratore["password"]

                        self.admin_homepage = HomepageAmministratore(admin)
                        self.admin_homepage.show()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Errore", "Credenziali o codice amministratore errati!")
                except FileNotFoundError as e:
                    QtWidgets.QMessageBox.critical(self, "Errore", str(e))
                except ValueError as e:
                    QtWidgets.QMessageBox.critical(self, "Errore", str(e))
            else:
                # Tentativo di login come cliente o dipendente
                try:
                    cliente = Cliente(None, None, None, None, None, username)
                    dati_cliente = cliente.accedi(username, password)
                    if dati_cliente:
                        cliente.nome = dati_cliente["nome"]
                        cliente.cognome = dati_cliente["cognome"]
                        cliente.email = dati_cliente["email"]
                        cliente.telefono = dati_cliente["telefono"]
                        cliente.password = dati_cliente["password"]

                        self.client_homepage = HomepageCliente(cliente)
                        self.client_homepage.show()
                    else:
                        # Verifica se è un dipendente
                        dipendente = Dipendente.accedi(username, password)
                        if dipendente:
                            self.employee_homepage = HomepageDipendente(dipendente)
                            self.employee_homepage.show()
                        else:
                            QtWidgets.QMessageBox.warning(self, "Errore", "Credenziali errate!")
                except FileNotFoundError as e:
                    QtWidgets.QMessageBox.critical(self, "Errore", str(e))
                except ValueError as e:
                    QtWidgets.QMessageBox.critical(self, "Errore", str(e))
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Inserire username e password!")

    def handle_register(self):
        self.registration_form = CreaAccount()
        self.registration_form.show()

    def show_password_recovery(self):
        self.recovery_window = PasswordRecoveryWindow()
        self.recovery_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())