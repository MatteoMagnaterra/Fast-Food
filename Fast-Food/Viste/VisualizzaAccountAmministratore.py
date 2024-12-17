import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Classi.Amministratore import Amministratore


class VisualizzaAccountAmministratore(QtWidgets.QWidget):
    def __init__(self, amministratore):
        super().__init__()
        self.amministratore = amministratore
        self.setWindowTitle("Fast-Food - Visualizza Account")
        self.setGeometry(150, 150, 500, 600)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel("Visualizza Account", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        layout.addWidget(title_label)

        form_layout = QtWidgets.QFormLayout()

        # Campi del modulo
        self.nome_edit = QtWidgets.QLineEdit()
        self.cognome_edit = QtWidgets.QLineEdit()
        self.email_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.telefono_edit = QtWidgets.QLineEdit()
        self.username_edit = QtWidgets.QLineEdit()
        self.codice_edit = QtWidgets.QLineEdit()

        # Disabilitare i campi in modo che non siano modificabili
        for widget in [self.nome_edit, self.cognome_edit, self.email_edit, self.password_edit,
                       self.telefono_edit, self.username_edit, self.codice_edit]:
            widget.setDisabled(True)

        # Campi del modulo aggiunti al layout
        form_layout.addRow("Nome", self.nome_edit)
        form_layout.addRow("Cognome", self.cognome_edit)
        form_layout.addRow("Email", self.email_edit)
        form_layout.addRow("Password", self.password_edit)
        form_layout.addRow("Telefono", self.telefono_edit)
        form_layout.addRow("Username", self.username_edit)
        form_layout.addRow("Codice", self.codice_edit)

        layout.addLayout(form_layout)

        # Aggiunta dei pulsanti per Modifica ed Elimina Account
        button_layout = QtWidgets.QHBoxLayout()

        self.modifica_button = QtWidgets.QPushButton()
        self.modifica_button.setIcon(QtGui.QIcon.fromTheme("edit"))
        self.modifica_button.setIconSize(QtCore.QSize(32, 32))
        self.modifica_button.setText("Modifica Account")

        self.elimina_button = QtWidgets.QPushButton()
        self.elimina_button.setIcon(QtGui.QIcon.fromTheme("delete"))
        self.elimina_button.setIconSize(QtCore.QSize(32, 32))
        self.elimina_button.setText("Elimina Account")

        button_layout.addWidget(self.modifica_button)
        button_layout.addWidget(self.elimina_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Collegamento dei pulsanti alle funzioni appropriate
        self.elimina_button.clicked.connect(self.elimina_account_amministratore)
        self.modifica_button.clicked.connect(self.modifica_account)

        # Caricamento dei dati dell'amministratore
        self.carica_dati_amministratore()

        # Flag per determinare se si sta modificando
        self.in_modifica = False

    def carica_dati_amministratore(self):
        """Carica i dati dell'amministratore dall'oggetto amministratore."""
        self.nome_edit.setText(self.amministratore.nome)
        self.cognome_edit.setText(self.amministratore.cognome)
        self.email_edit.setText(self.amministratore.email)
        self.password_edit.setText(self.amministratore.password)
        self.telefono_edit.setText(self.amministratore.telefono)
        self.username_edit.setText(self.amministratore.username)
        self.codice_edit.setText(self.amministratore.codice)

    def elimina_account_amministratore(self):
        """Elimina l'account dell'amministratore e torna alla schermata di accesso."""
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Conferma Eliminazione",
            "Sei sicuro di voler eliminare il tuo account? Questa operazione è irreversibile.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            # Chiama il metodo elimina_account dell'oggetto amministratore
            self.amministratore.elimina_account()
            QtWidgets.QMessageBox.information(self, "Account Eliminato",
                                              "Il tuo account è stato eliminato con successo.")
            self.close()

    def modifica_account(self):
        if not self.in_modifica:
            # Attiva la modalità di modifica
            for widget in [self.nome_edit, self.cognome_edit, self.email_edit, self.password_edit,
                           self.telefono_edit, self.username_edit, self.codice_edit]:
                widget.setDisabled(False)

            self.modifica_button.setText("Salva Modifiche")
            self.in_modifica = True
        else:
            # Raccogli i dati modificati
            nuovi_dati = {
                "nome": self.nome_edit.text(),
                "cognome": self.cognome_edit.text(),
                "email": self.email_edit.text(),
                "password": self.password_edit.text(),
                "telefono": self.telefono_edit.text(),
                "username": self.username_edit.text(),
                "codice": self.codice_edit.text()
            }

            # Chiama il metodo modifica_account dell'amministratore con i nuovi dati
            if self.amministratore.modifica_account(nuovi_dati):
                # Disabilita nuovamente i campi
                for widget in [self.nome_edit, self.cognome_edit, self.email_edit, self.password_edit,
                               self.telefono_edit, self.username_edit, self.codice_edit]:
                    widget.setDisabled(True)

                self.modifica_button.setText("Modifica Account")
                self.in_modifica = False

                QtWidgets.QMessageBox.information(self, "Successo",
                                                  "I dati dell'account sono stati aggiornati con successo.")
            else:
                QtWidgets.QMessageBox.warning(self, "Errore", "Username o codice già in uso. Scegli valori diversi.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    amministratore = Amministratore()
    window = VisualizzaAccountAmministratore(amministratore)
    window.show()
    sys.exit(app.exec())
