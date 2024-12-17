import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Classi.Prodotto import Prodotto


class VisualizzaPanini(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Visualizza Panini")
        self.setGeometry(150, 150, 700, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel("Visualizza Panini", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        main_layout.addWidget(title_label)

        # Filtro prodotti
        filter_layout = QtWidgets.QHBoxLayout()
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Filtra Prodotti")
        self.filter_button = QtWidgets.QPushButton("Apply")

        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(self.filter_button)

        main_layout.addLayout(filter_layout)

        # Elenco panini
        self.products_layout = QtWidgets.QVBoxLayout()

        # Caricamento dei panini dal magazzino
        panini = Prodotto.leggi_panini_da_magazzino("Magazzino.json")
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

        # Sezione ingredienti
        ingredient_layout = QtWidgets.QVBoxLayout()
        for ingredient in ingredients:
            ingredient_row = QtWidgets.QHBoxLayout()
            ingredient_label = QtWidgets.QLabel(ingredient)

            ingredient_row.addWidget(ingredient_label)
            ingredient_layout.addLayout(ingredient_row)

        # Sezione prezzo e punti
        price_label = QtWidgets.QLabel(f"€{price:.2f}  {points}p")
        price_label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addLayout(image_name_layout)
        layout.addLayout(ingredient_layout)
        layout.addWidget(price_label)

        return widget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaPanini()
    window.show()
    sys.exit(app.exec())