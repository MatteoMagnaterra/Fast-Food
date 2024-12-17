import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Viste.VisualizzaAccountAmministratore import VisualizzaAccountAmministratore
from Viste.VisualizzaDipendenti import VisualizzaDipendenti
from Viste.VisualizzaProdottiAmministratore import VisualizzaProdotti
from Viste.VisualizzaFeedback import VisualizzaFeedback
import threading
from Viste.Statistiche import main


class HomepageAmministratore(QtWidgets.QWidget):
    def __init__(self, amministratore):
        super().__init__()
        self.amministratore = amministratore
        self.setWindowTitle("Fast-Food - Homepage Amministratore")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Titolo della finestra
        title_label = QtWidgets.QLabel(f"Benvenuto {self.amministratore.nome}", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        layout.addWidget(title_label)

        # Pulsanti principali
        self.staff_button = QtWidgets.QPushButton("Visualizza Dettagli Dipendenti", self)
        self.products_button = QtWidgets.QPushButton("Visualizza Prodotti", self)
        self.feedback_button = QtWidgets.QPushButton("Visualizza Feedback", self)
        self.account_button = QtWidgets.QPushButton("Visualizza Account", self)
        self.statistiche_button = QtWidgets.QPushButton("Visualizza Statistiche", self)

        # Aggiunta dei pulsanti al layout
        layout.addWidget(self.staff_button)
        layout.addWidget(self.products_button)
        layout.addWidget(self.feedback_button)
        layout.addWidget(self.account_button)
        layout.addWidget(self.statistiche_button)

        self.account_button.clicked.connect(self.open_account_window)
        self.staff_button.clicked.connect(self.open_staff_window)
        self.products_button.clicked.connect(self.open_products_window)
        self.feedback_button.clicked.connect(self.open_feedback_window)
        self.statistiche_button.clicked.connect(self.open_statistiche_window)

        self.setLayout(layout)

    def open_account_window(self):
        self.account_window = VisualizzaAccountAmministratore(self.amministratore)
        self.account_window.show()

    def open_staff_window(self):
        self.staff_window = VisualizzaDipendenti(self.amministratore)
        self.staff_window.show()

    def open_products_window(self):
        self.products_window = VisualizzaProdotti()
        self.products_window.show()

    def open_feedback_window(self):
        print("Apertura finestra Feedback")
        self.feedback_window = VisualizzaFeedback()
        self.feedback_window.show()

    def open_statistiche_window(self):
        # Utilizza threading per non bloccare l'interfaccia utente Qt
        threading.Thread(target=main).start()  # Esegui la funzione main del codice Tkinter in un thread separato


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomepageAmministratore()
    window.show()
    sys.exit(app.exec())
