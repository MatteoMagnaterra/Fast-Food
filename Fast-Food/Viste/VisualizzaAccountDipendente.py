import sys
from PySide6 import QtCore, QtWidgets, QtGui
class VisualizzaAccountDipendente(QtWidgets.QWidget):
    def __init__(self, dipendente):
        super().__init__()
        self.dipendente = dipendente
        self.setWindowTitle("Fast-Food - Visualizza Account Dipendente")
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
        self.data_edit = QtWidgets.QLineEdit()
        self.email_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()  # La password sarà visibile
        self.telefono_edit = QtWidgets.QLineEdit()
        self.username_edit = QtWidgets.QLineEdit()

        # Disabilitare i campi in modo che non siano modificabili
        for widget in [self.nome_edit, self.cognome_edit, self.data_edit, self.email_edit, self.password_edit,
                       self.telefono_edit, self.username_edit]:
            widget.setDisabled(True)

        # Campi del modulo aggiunti al layout
        form_layout.addRow("Nome", self.nome_edit)
        form_layout.addRow("Cognome", self.cognome_edit)
        form_layout.addRow("Data di Nascita", self.data_edit)
        form_layout.addRow("Email", self.email_edit)
        form_layout.addRow("Password", self.password_edit)  # La password ora sarà visibile
        form_layout.addRow("Telefono", self.telefono_edit)
        form_layout.addRow("Username", self.username_edit)

        layout.addLayout(form_layout)

        # Caricamento dei dati dell'utente
        self.carica_dati_cliente()

    def carica_dati_cliente(self):
        """Carica i dati del dipendente dal dizionario."""
        self.nome_edit.setText(self.dipendente["nome"])
        self.cognome_edit.setText(self.dipendente["cognome"])
        self.data_edit.setText(self.dipendente["data_di_nascita"])
        self.email_edit.setText(self.dipendente["email"])
        self.password_edit.setText(self.dipendente["password"])  # Visualizza la password in chiaro
        self.telefono_edit.setText(self.dipendente["telefono"])
        self.username_edit.setText(self.dipendente["username"])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaAccountDipendente()
    window.show()
    sys.exit(app.exec())

