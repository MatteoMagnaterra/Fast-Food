import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Viste.VisualizzaPanini1 import VisualizzaPanini1
from Viste.VisualizzaContorni1 import VisualizzaContorni1
from Viste.VisualizzaBevande1 import VisualizzaBevande1
from Viste.VisualizzaDolci1 import VisualizzaDolci1
from Viste.RiepilogoOrdine import RiepilogoOrdine


class EffettuaOrdine(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Effettua Ordine")
        self.setGeometry(200, 100, 800, 600)
        self.cart_products = []  # Lista dei prodotti nell'ordine
        self.order_count = 0  # Contatore prodotti nell'ordine
        self.init_ui()

    def init_ui(self):
        # Layout principale
        main_layout = QtWidgets.QVBoxLayout(self)

        # Header senza collegamenti cliccabili
        header_layout = QtWidgets.QHBoxLayout()
        self.header_label = QtWidgets.QLabel('Effettua Ordine')
        self.header_label.setAlignment(QtCore.Qt.AlignLeft)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Bottone Ordine in alto a destra
        self.order_button = QtWidgets.QPushButton(f"Ordine({self.order_count})")
        self.order_button.setFont(QtGui.QFont("Arial", 12))
        self.order_button.clicked.connect(self.view_order_summary)
        header_layout.addWidget(self.order_button)

        main_layout.addLayout(header_layout)

        # Titolo
        title = QtWidgets.QLabel("Aggiungi prodotti all'Ordine!")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title)

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
        """Apre la finestra VisualizzaPanini1 per i panini."""
        self.panini_window = VisualizzaPanini1(cart_products=self.cart_products, order_button=self.order_button)
        self.panini_window.show()

    def open_visualizza_contorni(self):
        """Apre la finestra VisualizzaContorni per i contorni."""
        self.contorni_window = VisualizzaContorni1(cart_products=self.cart_products, order_button=self.order_button)
        self.contorni_window.show()

    def open_visualizza_bevande(self):
        """Apre la finestra VisualizzaBevande per le bevande."""
        self.bevande_window = VisualizzaBevande1(cart_products=self.cart_products, order_button=self.order_button)
        self.bevande_window.show()

    def open_visualizza_dolci(self):
        """Apre la finestra VisualizzaDolci per i dolci."""
        self.dolci_window = VisualizzaDolci1(cart_products=self.cart_products, order_button=self.order_button)
        self.dolci_window.show()

    def view_order_summary(self):
        """Mostra il riepilogo dell'ordine."""
        cliente_email = "cliente@example.com"  # Sostituisci con l'email effettiva del cliente
        self.riepilogo_window = RiepilogoOrdine(self.cart_products, self.order_button, cliente_email)
        self.riepilogo_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EffettuaOrdine()
    window.show()
    sys.exit(app.exec())