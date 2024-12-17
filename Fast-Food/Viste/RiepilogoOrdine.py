import sys
from PySide6 import QtCore, QtWidgets, QtGui
import json
from datetime import datetime
from Gestori.GestoreJSON import GestoreJSON
import random
import string


class RiepilogoOrdine(QtWidgets.QWidget):
    def __init__(self, cart_products, order_button, cliente_email):
        super().__init__()
        self.gestore_json = GestoreJSON()  # Inizializza GestoreJSON
        self.setWindowTitle("Fast-Food - Riepilogo Ordine")
        self.setGeometry(150, 150, 700, 600)
        self.order_products = cart_products
        self.order_button = order_button
        self.cliente_email = cliente_email
        self.init_ui()

    def confirm_order(self):
        totale_prezzo, totale_punti = self.calculate_totals()

        ordine = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "codice_ordine": genera_codiceunivoco(),
            "stato_ordine": "In Esecuzione",
            "prodotti": [
                {
                    "nome": product["nome"],
                    "ingredienti": product["ingredienti"],
                    "prezzo": product["prezzo"],
                    "punti": product["punti"],
                    "tipo": product.get("tipo", "Sconosciuto")
                }
                for product in self.order_products
            ],
            "totale": {
                "prezzo": totale_prezzo,
                "punti": totale_punti,
            }
        }

        # Salva l'ordine nel file Ordini.json
        try:
            with open(self.gestore_json.ordini_file, "r") as file:
                ordini = json.load(file)
        except FileNotFoundError:
            ordini = []

        ordini.append(ordine)

        with open("Ordini.json", "w") as file:
            json.dump(ordini, file, indent=4)

        # Aggiorna il magazzino
        self.aggiorna_magazzino()

        # Mostra la ricevuta
        ricevuta = "\n".join([
            f"- {product['nome']} (€{product['prezzo']:.2f}, {product['punti']} punti)"
            for product in self.order_products
        ])
        totale = ordine["totale"]
        ricevuta += f"\n\nTotale: €{totale['prezzo']:.2f}\nPunti: {totale['punti']}"

        QtWidgets.QMessageBox.information(self, "Ricevuta", f"Ordine confermato!\n\n{ricevuta}")

        self.order_products.clear()
        self.update_order_list()
        self.order_button.setText("Ordine(0)")
        self.close()

    def aggiorna_magazzino(self):
        #Aggiorna il magazzino diminuendo la quantità dei prodotti ordinati.

        # Conta le occorrenze dei prodotti nell'ordine
        occorrenze = self.conta_occorrenze(self.order_products)

        # Carica il magazzino
        magazzino = self.gestore_json.load_magazzino()

        # Aggiorna il magazzino
        for categoria, prodotti in magazzino.items():
            for prodotto in prodotti:
                nome_prodotto = prodotto['nome']
                if nome_prodotto in occorrenze:
                    quantita_da_scalare = occorrenze[nome_prodotto]
                    if prodotto.get("quantita'", 0) >= quantita_da_scalare:  # Nota l'uso di "quantita'"
                        prodotto["quantita'"] -= quantita_da_scalare  # Nota l'uso di "quantita'"
                        print(f"Quantità aggiornata per '{nome_prodotto}': {prodotto['quantita\'']}")
                    else:
                        QtWidgets.QMessageBox.warning(
                            self, "Errore Magazzino",
                            f"Il prodotto '{nome_prodotto}' ha quantità insufficiente per soddisfare l'ordine."
                        )

        # Salva il magazzino aggiornato
        self.gestore_json.save_magazzino(magazzino)

    def conta_occorrenze(self, order_products):

        #Conta le occorrenze di ogni prodotto nell'ordine.
        from collections import Counter
        return Counter(product['nome'] for product in order_products)

    def cancel_order(self):
        # Svuota la lista dei prodotti nell'ordine
        self.order_products.clear()
        # Aggiorna la visualizzazione dell'ordine
        self.update_order_list()
        # Aggiorna il pulsante Ordine()
        self.order_button.setText("Ordine(0)")
        # Mostra un messaggio di conferma
        QtWidgets.QMessageBox.warning(self, "Ordine Annullato", "Il tuo ordine è stato annullato.")
        self.close()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Riepilogo Ordine", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title_label)

        # Scroll Area Setup
        self.scroll_area = QtWidgets.QScrollArea(self)  # Crea l'area scrollabile
        self.scroll_area.setWidgetResizable(True)  # Rende il widget interno adattabile alle dimensioni dello scroll

        # Lista ordine
        self.container_widget = QtWidgets.QWidget(self)
        self.order_list_layout = QtWidgets.QVBoxLayout(self.container_widget)

        self.update_order_list()

        self.scroll_area.setWidget(self.container_widget)  # Imposta il widget contenitore come widget dello scroll area
        main_layout.addWidget(self.scroll_area)  # Aggiungi lo scroll area al layout principale

        main_layout.addLayout(self.order_list_layout)

        # Sezione pulsanti
        button_layout = QtWidgets.QHBoxLayout()
        confirm_button = QtWidgets.QPushButton("Conferma Ordine")
        confirm_button.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        confirm_button.clicked.connect(self.confirm_order)

        cancel_button = QtWidgets.QPushButton("Annulla Ordine")
        cancel_button.setStyleSheet("background-color: red; color: white; font-size: 16px;")
        cancel_button.clicked.connect(self.cancel_order)

        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_order_list(self):
        # Svuota il layout esistente
        while self.order_list_layout.count():
            child = self.order_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        total_price = 0
        total_points = 0

        for product in self.order_products:
            # Creazione del widget del prodotto
            product_widget = self.create_product_widget(
                product['nome'], product['ingredienti'], product['prezzo'], product['punti'],
                product.get('tipo', 'Panino')
            )
            self.order_list_layout.addWidget(product_widget)

            total_price += product['prezzo']
            total_points += product['punti']

        # Totale
        if total_price > 0 or total_points > 0:  # Mostra il totale solo se ci sono prodotti
            discounted_price = self.apply_discount(total_price, total_points)
            total_label = QtWidgets.QLabel(f"Totale: €{discounted_price:.2f}  Punti: {total_points}")
            total_label.setAlignment(QtCore.Qt.AlignRight)
            total_label.setFont(QtGui.QFont("Arial", 14))
            self.order_list_layout.addWidget(total_label)

    def create_product_widget(self, name, ingredients, price, points, tipo):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        # Sezione immagine e nome prodotto
        image_name_layout = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel(name)
        name_label.setFont(QtGui.QFont("Arial", 14))
        name_label.setAlignment(QtCore.Qt.AlignCenter)

        image_label = QtWidgets.QLabel()

        # Determina l'icona in base al tipo di prodotto
        if tipo == "Panino":
            image_label.setText("🍔")
        elif tipo == "Bevanda":
            image_label.setText("🥤")
        elif tipo == "Contorno":
            image_label.setText("🍟")
        elif tipo == "Dolce":
            image_label.setText("🍨")
        else:
            image_label.setText("❓")  # Fallback per tipi non riconosciuti

        image_label.setAlignment(QtCore.Qt.AlignCenter)
        image_label.setFont(QtGui.QFont("Arial", 50))

        image_name_layout.addWidget(name_label)
        image_name_layout.addWidget(image_label)

        # Sezione ingredienti
        ingredient_layout = QtWidgets.QVBoxLayout()
        for ingredient in ingredients:
            ingredient_label = QtWidgets.QLabel(ingredient)
            ingredient_label.setFont(QtGui.QFont("Arial", 10))
            ingredient_layout.addWidget(ingredient_label)

        # Sezione prezzo
        price_label = QtWidgets.QLabel(f"€{price:.2f}")
        price_label.setFont(QtGui.QFont("Arial", 14))
        price_label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addLayout(image_name_layout)
        layout.addLayout(ingredient_layout)
        layout.addWidget(price_label)

        return widget
   
    def apply_discount(self, total_price, total_points):
        """Applica uno sconto di 2€ ogni 20 punti."""
        discount = (total_points // 20) * 2
        return max(0, total_price - discount)

    def calculate_totals(self):
        """Calcola il totale del prezzo e dei punti, applicando lo sconto."""
        total_price = sum(product['prezzo'] for product in self.order_products)
        total_points = sum(product['punti'] for product in self.order_products)
        discounted_price = self.apply_discount(total_price, total_points)
        return discounted_price, total_points

def genera_codiceunivoco():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RiepilogoOrdine([], QtWidgets.QPushButton("Ordine(0)"))
    window.show()
    sys.exit(app.exec())