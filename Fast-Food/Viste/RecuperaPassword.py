import sys
from PySide6 import QtCore, QtWidgets


class PasswordRecoveryWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Dimenticata")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()
        email_label = QtWidgets.QLabel("Email:")
        self.email_input = QtWidgets.QLineEdit(self)
        form_layout.addRow(email_label, self.email_input)

        self.recovery_button = QtWidgets.QPushButton("Richiedi Nuova Password", self)
        self.recovery_button.clicked.connect(self.handle_recovery)

        layout.addLayout(form_layout)
        layout.addWidget(self.recovery_button, alignment=QtCore.Qt.AlignCenter)

    def handle_recovery(self):
        email = self.email_input.text()
        # Chiamata al metodo del gestore utente per gestire la richiesta di recupero
        QtWidgets.QMessageBox.information(self, "Recupero Password", f"Una richiesta di recupero password è stata inviata a: {email}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PasswordRecoveryWindow()
    window.show()
    app.exec()
