import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from Viste.VisualizzaListaOrdiniClienti import VisualizzaListaOrdiniClienti
from Viste.VisualizzaAccountDipendente import VisualizzaAccountDipendente
from Viste.VisualizzaScorteMagazzino import VisualizzaScorteMagazzino


class HomepageDipendente(QWidget):
    def __init__(self, dipendente):
        super().__init__()
        self.dipendente = dipendente
        self.init_ui()

    def init_ui(self):
        # Configurazione della finestra principale
        self.setWindowTitle('Fast-Food - Homepage Dipendente')
        self.setGeometry(100, 100, 600, 400)

        # Creazione del layout principale
        layout = QVBoxLayout()

        # Etichetta di benvenuto dinamica
        homepage_label = QLabel(f'Ciao, {self.dipendente["nome"]} {self.dipendente["cognome"]}')
        homepage_label.setAlignment(QtCore.Qt.AlignCenter)  # Centrare il testo dell'etichetta
        layout.addWidget(homepage_label)

        # Creazione dei bottoni
        btn_order_details = QPushButton('Visualizza Lista Dettagli Ordini')
        btn_inventory = QPushButton('Visualizza Scorte Magazzino')
        btn_account_details = QPushButton('Visualizza Account Dipendente')

        # Collegamento dei pulsanti alle relative funzioni
        btn_order_details.clicked.connect(self.show_order_details)
        btn_inventory.clicked.connect(self.show_inventory)
        btn_account_details.clicked.connect(self.show_account_details)

        # Aggiunta dei pulsanti al layout
        layout.addWidget(btn_order_details)
        layout.addWidget(btn_inventory)
        layout.addWidget(btn_account_details)

        # Impostazione del layout principale
        self.setLayout(layout)

    def show_order_details(self):
        """Mostra la finestra con i dettagli degli ordini."""
        self.show_order_detail = VisualizzaListaOrdiniClienti()
        self.show_order_detail.show()

    def show_inventory(self):
        """Mostra la finestra con le scorte del magazzino."""
        self.show_inventory = VisualizzaScorteMagazzino()
        self.show_inventory.show()

    def show_account_details(self):
        """Mostra la finestra con i dettagli dell'account del dipendente."""
        self.account_details_window = VisualizzaAccountDipendente(self.dipendente)
        self.account_details_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomepageDipendente()
    window.show()
    sys.exit(app.exec())
