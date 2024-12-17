import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Classi.Prodotto import Prodotto
from Gestori.GestoreJSON import GestoreJSON


class VisualizzaPanini1(QtWidgets.QWidget):
    def __init__(self,cart_products, order_button):
        super().__init__()
        self.setWindowTitle("Fast-Food - Visualizza Panini")
        self.setGeometry(150, 150, 700, 600)
        self.cart_products = cart_products  # Lista condivisa dei prodotti nel carrello
        self.order_button = order_button  # Riferimento al pulsante "Ordine"
        self.gestore_json = GestoreJSON()
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Visualizza Panini", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title_label)

        # Elenco panini
        self.products_layout = QtWidgets.QVBoxLayout()

        # Caricamento dei panini dal magazzino
        panini = Prodotto.leggi_panini_da_magazzino(self.gestore_json.magazzino_file)
        for panino in panini:
            product_widget = self.create_product_widget(
                panino.nome, panino.ingredienti, panino.prezzo, panino.punti
            )
            self.products_layout.addWidget(product_widget)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_content.setLayout(self.products_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_product_widget(self, name, ingredients, price, points):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        # Sezione immagine e nome panino
        image_name_layout = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel(name)
        name_label.setFont(QtGui.QFont("Arial", 14))
        name_label.setAlignment(QtCore.Qt.AlignCenter)

        image_label = QtWidgets.QLabel()
        image_label.setText("🍔")
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        image_label.setFont(QtGui.QFont("Arial", 50))

        image_name_layout.addWidget(name_label)
        image_name_layout.addWidget(image_label)
        layout.addLayout(image_name_layout)

        # Lista degli ingredienti aggiornabile
        current_ingredients = ingredients[:]
        ingredient_layout = QtWidgets.QVBoxLayout()

        for ingredient in ingredients:
            ingredient_row = QtWidgets.QHBoxLayout()
            ingredient_label = QtWidgets.QLabel(ingredient)

            ingredient_row.addWidget(ingredient_label)
            ingredient_layout.addLayout(ingredient_row)

        layout.addLayout(ingredient_layout)

        # Prezzo e bottone aggiungi
        price_label = QtWidgets.QLabel(f"€{price:.2f}  {points}p")
        price_label.setAlignment(QtCore.Qt.AlignCenter)
        add_button = QtWidgets.QPushButton("Aggiungi all'ordine")

        # Funzione per aggiungere all'ordine
        def add_to_order():
            # Usa gli ingredienti aggiornati
            modified_product = {
                "nome": name,
                "ingredienti": current_ingredients[:],  # Lista aggiornata
                "prezzo": price,
                "punti": points,
                "tipo": "Panino"
            }
            self.cart_products.append(modified_product)
            current_count = int(self.order_button.text().split('(')[1].strip(')'))
            self.order_button.setText(f"Ordine({current_count + 1})")

        add_button.clicked.connect(add_to_order)

        layout.addWidget(price_label)
        layout.addWidget(add_button)

        return widget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    cart_products = []  # Lista vuota per i prodotti nel carrello
    order_button = QtWidgets.QPushButton("Ordine(0)")  # Pulsante per visualizzare il numero di ordini
    window = VisualizzaPanini1(cart_products=cart_products, order_button=order_button)
    window.show()
    sys.exit(app.exec())