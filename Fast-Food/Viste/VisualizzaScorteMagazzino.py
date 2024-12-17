'''
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Gestori.GestoreJSON import GestoreJSON

class VisualizzaScorteMagazzino(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Scorte Magazzino")
        self.setGeometry(200, 100, 800, 600)
        self.gestore_json = GestoreJSON()
        self.magazzino = self.gestore_json.load_magazzino()

        self.init_ui()
        self.setup_stock_monitor()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Visualizzazione Scorte di Magazzino")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        main_layout.addWidget(title_label)

        # Layout per le categorie e le quantità
        stock_layout = QtWidgets.QVBoxLayout()

        for category, products in self.magazzino.items():
            # Etichetta per ogni categoria
            category_label = QtWidgets.QLabel(f"<b>{category.capitalize()}</b>")
            category_label.setAlignment(QtCore.Qt.AlignLeft)
            category_label.setFont(QtGui.QFont("Arial", 18))
            stock_layout.addWidget(category_label)

            for product in products:
                product_name = product.get('nome', 'Sconosciuto')
                quantity = product.get("quantita'", 'Nulla')
                price = product.get('prezzo', 'N/A')
                points = product.get('punti', 'N/A')

                # Layout orizzontale per il prodotto
                product_layout = QtWidgets.QHBoxLayout()

                # Etichetta del prodotto
                product_label = QtWidgets.QLabel(
                    f"- {product_name}: {quantity} unità | Prezzo: €{price:.2f} | Punti: {points}"
                )
                product_label.setAlignment(QtCore.Qt.AlignLeft)
                product_label.setFont(QtGui.QFont("Arial", 14))
                product_label.setStyleSheet("color: #555;")
                product_layout.addWidget(product_label)

                # Pulsante per resettare la quantità
                reset_button = QtWidgets.QPushButton("Reset Quantità")
                reset_button.setFixedSize(120, 30)
                reset_button.clicked.connect(
                    lambda _, cat=category, name=product_name, label=product_label: self.reset_quantita(cat, name, label)
                )
                product_layout.addWidget(reset_button)

                stock_layout.addLayout(product_layout)

        # Aggiungi il layout principale
        main_layout.addLayout(stock_layout)
        self.setLayout(main_layout)

    def reset_quantita(self, categoria, nome_prodotto, product_label):
        #Metodo per resettare la quantità di un prodotto a una quantità predefinita.

        try:
            nuova_quantita = 100  # Imposta il valore predefinito per la quantità
            self.gestore_json.reset_quantita_prodotto(categoria, nome_prodotto, nuova_quantita)
            QtWidgets.QMessageBox.information(
                self, "Successo", f"Quantità del prodotto '{nome_prodotto}' resettata!"
            )
            # Aggiorna solo l'etichetta del prodotto
            product_label.setText(
                product_label.text().replace(
                    product_label.text().split(':')[1].split('unità')[0],
                    f" {nuova_quantita} "
                )
            )
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Errore", str(e))

    def setup_stock_monitor(self):
        self.stock_timer = QtCore.QTimer(self)
        self.stock_timer.timeout.connect(self.check_stock_levels)
        self.stock_timer.start(300000)  # Controlla ogni 5 minuti

    def check_stock_levels(self):
        for category, products in self.magazzino.items():
            for product in products:
                product_name = product.get('nome', 'Sconosciuto')
                quantity = product.get("quantita'", 0)

                if quantity <= 10:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Attenzione",
                        f"ATTENZIONE, il prodotto '{product_name}' ha solo {quantity} unità rimaste. Si prega di rifornirlo!"
                    )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaScorteMagazzino()
    window.show()
    sys.exit(app.exec())'''


import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Gestori.GestoreJSON import GestoreJSON


class VisualizzaScorteMagazzino(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Scorte Magazzino")
        self.setGeometry(200, 100, 800, 600)
        self.gestore_json = GestoreJSON()
        self.magazzino = self.gestore_json.load_magazzino()

        self.init_ui()
        self.setup_stock_monitor()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Visualizzazione Scorte di Magazzino")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        main_layout.addWidget(title_label)

        # Creazione dello scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permette il ridimensionamento automatico

        # Widget contenitore per lo scroll
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # Layout per le categorie e le quantità
        for category, products in self.magazzino.items():
            # Etichetta per ogni categoria
            category_label = QtWidgets.QLabel(f"<b>{category.capitalize()}</b>")
            category_label.setAlignment(QtCore.Qt.AlignLeft)
            category_label.setFont(QtGui.QFont("Arial", 18))
            scroll_layout.addWidget(category_label)

            for product in products:
                product_name = product.get('nome', 'Sconosciuto')
                quantity = product.get("quantita'", 'Nulla')
                price = product.get('prezzo', 'N/A')
                points = product.get('punti', 'N/A')

                # Layout orizzontale per il prodotto
                product_layout = QtWidgets.QHBoxLayout()

                # Etichetta del prodotto
                product_label = QtWidgets.QLabel(
                    f"- {product_name}: {quantity} unità | Prezzo: €{price:.2f} | Punti: {points}"
                )
                product_label.setAlignment(QtCore.Qt.AlignLeft)
                product_label.setFont(QtGui.QFont("Arial", 14))
                product_label.setStyleSheet("color: #555;")
                product_layout.addWidget(product_label)

                # Pulsante per resettare la quantità
                reset_button = QtWidgets.QPushButton("Reset Quantità")
                reset_button.setFixedSize(120, 30)
                reset_button.clicked.connect(
                    lambda _, cat=category, name=product_name, label=product_label: self.reset_quantita(cat, name,
                                                                                                        label)
                )
                product_layout.addWidget(reset_button)

                scroll_layout.addLayout(product_layout)

        # Aggiungi il widget con il layout allo scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def reset_quantita(self, categoria, nome_prodotto, product_label):
        """
        Metodo per resettare la quantità di un prodotto a una quantità predefinita.
        Aggiorna immediatamente l'etichetta della quantità resettata.
        """
        try:
            nuova_quantita = 100  # Imposta il valore predefinito per la quantità
            self.gestore_json.reset_quantita_prodotto(categoria, nome_prodotto, nuova_quantita)
            QtWidgets.QMessageBox.information(
                self, "Successo", f"Quantità del prodotto '{nome_prodotto}' resettata!"
            )
            # Aggiorna solo l'etichetta del prodotto
            product_label.setText(
                product_label.text().replace(
                    product_label.text().split(':')[1].split('unità')[0],
                    f" {nuova_quantita} "
                )
            )
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Errore", str(e))

    def setup_stock_monitor(self):
        """
        Configura un timer per controllare periodicamente le scorte di magazzino
        e mostrare un avviso se qualche prodotto ha quantità uguale o inferiore a 10.
        """
        self.stock_timer = QtCore.QTimer(self)
        self.stock_timer.timeout.connect(self.check_stock_levels)
        self.stock_timer.start(60000)  # Controlla ogni 5 minuti

    def check_stock_levels(self):
        """
        Controlla se qualche prodotto ha quantità uguale o inferiore a 10
        e mostra una notifica di avviso.
        """
        for category, products in self.magazzino.items():
            for product in products:
                product_name = product.get('nome', 'Sconosciuto')
                quantity = product.get("quantita'", 0)

                if quantity <= 10:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Attenzione",
                        f"ATTENZIONE, il prodotto '{product_name}' ha solo {quantity} unità rimaste. "
                        f"Si prega di rifornirlo!"
                    )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaScorteMagazzino()
    window.show()
    sys.exit(app.exec())


