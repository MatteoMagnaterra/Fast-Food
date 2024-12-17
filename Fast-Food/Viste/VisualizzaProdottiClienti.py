import sys
import json
from PySide6 import QtCore, QtWidgets, QtGui
from Gestori.GestoreJSON import GestoreJSON
from Viste.VisualizzaPanini import VisualizzaPanini
from Viste.VisualizzaContorni import VisualizzaContorni
from Viste.VisualizzaBevande import VisualizzaBevande
from Viste.VisualizzaDolci import VisualizzaDolci


class VisualizzaProdottiCliente(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Effettua Ordine")
        self.setGeometry(200, 100, 800, 600)
        self.init_ui()
        self.gestore_json = GestoreJSON()
        self.magazzino = self.load_magazzino()

    def init_ui(self):
        # Layout principale
        main_layout = QtWidgets.QVBoxLayout(self)

        # Header senza collegamenti cliccabili e senza carrello
        header_layout = QtWidgets.QHBoxLayout()
        self.header_label = QtWidgets.QLabel('Effettua Ordine | Visualizza Prodotti | Visualizza Account')
        self.header_label.setAlignment(QtCore.Qt.AlignLeft)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Titolo
        title = QtWidgets.QLabel("Visualizza Prodotti")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title)

        # Barra di filtro
        filter_layout = QtWidgets.QVBoxLayout()
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Cerca un prodotto nel menù...")
        self.filter_input.textChanged.connect(self.filter_products)
        filter_layout.addWidget(self.filter_input)

        self.filter_results = QtWidgets.QListWidget()
        self.filter_results.hide()  # Nasconde la lista inizialmente
        filter_layout.addWidget(self.filter_results)

        main_layout.addLayout(filter_layout)

        # Icone principali
        icons_layout = QtWidgets.QGridLayout()
        icons = [
            ("Panino", "🍔"),
            ("Contorno", "🍟"),
            ("Bevande", "🥤"),
            ("Dolce", "🍨"),
        ]

        for i, (label, icon) in enumerate(icons):
            button = QtWidgets.QPushButton(icon)
            button.setFont(QtGui.QFont("Arial", 40))
            button.setFixedSize(120, 120)
            if label == "Panino":
                button.clicked.connect(self.open_visualizza_panini)
            elif label == "Contorno":
                button.clicked.connect(self.open_visualizza_contorni)
            elif label == "Bevande":
                button.clicked.connect(self.open_visualizza_bevande)
            elif label == "Dolce":
                button.clicked.connect(self.open_visualizza_dolci)
            else:
                button.clicked.connect(lambda _, lbl=label: self.icon_clicked(lbl))

            # Calcola la posizione
            row = i // 2  # Riga in base all'indice
            col = i % 2  # Colonna in base all'indice

            # Aggiungi il pulsante nella griglia
            icons_layout.addWidget(button, row * 2, col)

            # Aggiungi l'etichetta sotto il pulsante
            label_widget = QtWidgets.QLabel(label, alignment=QtCore.Qt.AlignCenter)
            icons_layout.addWidget(label_widget, row * 2 + 1, col)

        main_layout.addLayout(icons_layout)

        self.setLayout(main_layout)

    def icon_clicked(self, label):
        """Funzione chiamata quando viene cliccata un'icona."""
        QtWidgets.QMessageBox.information(self, "Icona Cliccata", f"Hai cliccato su {label}!")

    def open_visualizza_panini(self):
        """Apre la finestra VisualizzaProdotti2 per i panini."""
        self.panini_window = VisualizzaPanini()
        self.panini_window.show()

    def open_visualizza_contorni(self):
        """Apre la finestra VisualizzaContorni per i contorni."""
        self.contorni_window = VisualizzaContorni()
        self.contorni_window.show()

    def open_visualizza_bevande(self):
        """Apre la finestra VisualizzaContorni per i contorni."""
        self.bevande_window = VisualizzaBevande()
        self.bevande_window.show()

    def open_visualizza_dolci(self):
        """Apre la finestra VisualizzaContorni per i contorni."""
        self.dolci_window = VisualizzaDolci()
        self.dolci_window.show()

    def filter_products(self):
        """Filtra i prodotti in base al testo inserito, cercando sia nel nome che negli ingredienti."""
        search_text = self.filter_input.text().lower()
        self.filter_results.clear()

        if search_text:
            for category, products in self.magazzino.items():
                for product in products:
                    # Controlla se il testo è nel nome o negli ingredienti
                    if (search_text in product['nome'].lower() or
                            any(search_text in ingredient.lower() for ingredient in product.get('ingredienti', []))):
                        self.filter_results.addItem(f"{product['nome']} ({category})")
            self.filter_results.setVisible(self.filter_results.count() > 0)
        else:
            self.filter_results.hide()

    def load_magazzino(self):
        """Carica i dati dei prodotti dal file Magazzino.json."""
        try:
            with open(self.gestore_json.magazzino_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, "Errore", "Il file Magazzino.json non è stato trovato.")
            return {}
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.critical(self, "Errore", "Errore nel leggere il file Magazzino.json.")
            return {}


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaProdottiCliente()
    window.show()
    sys.exit(app.exec())