import sys
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QDoubleValidator, QIntValidator


class VisualizzaProdotti(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast-Food - Visualizza Prodotti")
        self.setGeometry(200, 100, 800, 600)
        self.magazzino_file = "Magazzino.json"
        self.magazzino = self.load_magazzino()
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Barra di filtro
        filter_layout = QtWidgets.QVBoxLayout()
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Cerca un prodotto specifico...")
        self.filter_input.textChanged.connect(self.filter_products)
        filter_layout.addWidget(self.filter_input)

        self.filter_results = QtWidgets.QListWidget()
        self.filter_results.hide()  # Nasconde la lista inizialmente
        filter_layout.addWidget(self.filter_results)

        main_layout.addLayout(filter_layout)


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
            button.clicked.connect(lambda _, lbl=label: self.open_category_screen(lbl))
            row = i // 2
            col = i % 2
            icons_layout.addWidget(button, row * 2, col)
            label_widget = QtWidgets.QLabel(label, alignment=QtCore.Qt.AlignCenter)
            icons_layout.addWidget(label_widget, row * 2 + 1, col)

        main_layout.addLayout(icons_layout)
        self.setLayout(main_layout)

    def load_magazzino(self):
        try:
            with open(self.magazzino_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, "Errore", "Il file Magazzino.json non è stato trovato.")
            return {}
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.critical(self, "Errore", "Errore nel leggere il file Magazzino.json.")
            return {}

    def save_magazzino(self):
        try:
            with open(self.magazzino_file, "w") as file:
                json.dump(self.magazzino, file, indent=4)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Errore", f"Errore nel salvare il file Magazzino.json: {str(e)}")

    def open_category_screen(self, category):
        mapping = {
            "Panino": "panini",
            "Bevande": "bevande",
            "Contorno": "contorni",
            "Dolce": "dolci"
        }

        categoria = mapping.get(category)
        if not categoria:
            QtWidgets.QMessageBox.warning(self, "Errore", f"Categoria {category} non trovata.")
            return

        prodotti = self.magazzino.get(categoria, [])
        self.open_product_editor(categoria, prodotti)

    def filter_products(self):
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

    def open_product_editor(self, category, products):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Fast-Food - {category}")
        dialog.setGeometry(300, 150, 600, 400)

        layout = QtWidgets.QVBoxLayout(dialog)

        product_list = QtWidgets.QListWidget()
        product_list.addItems([product['nome'] for product in products])
        layout.addWidget(product_list)

        def edit_product():
            selected_item = product_list.currentItem()
            if selected_item:
                product_name = selected_item.text()
                product = next((p for p in products if p['nome'] == product_name), None)
                if product:
                    self.edit_product(dialog, product, products, category)

        def delete_product():
            selected_item = product_list.currentItem()
            if selected_item:
                product_name = selected_item.text()
                nonlocal products
                products = [p for p in products if p['nome'] != product_name]
                product_list.clear()
                product_list.addItems([p['nome'] for p in products])
                self.magazzino[category] = products
                self.save_magazzino()

        def add_product():
            details, ok = QtWidgets.QInputDialog.getText(
                dialog,
                "Aggiungi Nuovo Prodotto",
                "Inserisci nome, prezzo, punti e quantità del prodotto (separati da virgole):"
            )
            if ok and details:
                details = details.split(',')
                if len(details) >= 3:
                    try:
                        new_product = {
                            'nome': details[0].strip(),
                            'ingredienti': [],
                            'prezzo': float(details[1].strip().replace(',', '.')),
                            'punti': int(details[2].strip()),
                            'quantita': int(details[3].strip()) if len(details) > 3 else 100  # Quantità predefinita: 100
                        }
                        products.append(new_product)
                        product_list.clear()
                        product_list.addItems([p['nome'] for p in products])
                        self.magazzino[category] = products
                        self.save_magazzino()
                        QtWidgets.QMessageBox.information(dialog, "Successo",
                                                          f"Prodotto '{new_product['nome']}' aggiunto con successo!")
                    except ValueError:
                        QtWidgets.QMessageBox.warning(dialog, "Errore, Prezzo, punti o quantità non validi."
                                                              " Assicurati di inserire numeri validi.")


        edit_button = QtWidgets.QPushButton("Modifica Prodotto Selezionato")
        edit_button.clicked.connect(edit_product)
        layout.addWidget(edit_button)

        delete_button = QtWidgets.QPushButton("Elimina Prodotto Selezionato")
        delete_button.clicked.connect(delete_product)
        layout.addWidget(delete_button)

        add_button = QtWidgets.QPushButton("Aggiungi Nuovo Prodotto")
        add_button.clicked.connect(add_product)
        layout.addWidget(add_button)

        dialog.exec()

    def edit_product(self, parent, product, products, category):
        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Modifica Prodotto")
        dialog.setGeometry(350, 200, 400, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        ingredients_list = QtWidgets.QListWidget()
        ingredients_list.addItems(product.get('ingredienti', []))
        layout.addWidget(ingredients_list)

        def add_ingredient():
            text, ok = QtWidgets.QInputDialog.getText(dialog, "Aggiungi Ingrediente", "Inserisci l'ingrediente:")
            if ok and text:
                ingredients_list.addItem(text)

        def remove_ingredient():
            for item in ingredients_list.selectedItems():
                ingredients_list.takeItem(ingredients_list.row(item))

        btn_layout = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Aggiungi Ingrediente")
        add_btn.clicked.connect(add_ingredient)
        btn_layout.addWidget(add_btn)

        remove_btn = QtWidgets.QPushButton("Rimuovi Ingrediente")
        remove_btn.clicked.connect(remove_ingredient)
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)

        price_edit = QtWidgets.QLineEdit(str(product.get('prezzo', 0.0)))
        price_edit.setValidator(QDoubleValidator(0.99, 999.99, 2))
        points_edit = QtWidgets.QLineEdit(str(product.get('punti', 0)))
        points_edit.setValidator(QIntValidator(0, 1000))

        price_layout = QtWidgets.QHBoxLayout()
        price_layout.addWidget(QtWidgets.QLabel("Prezzo:"))
        price_layout.addWidget(price_edit)
        points_layout = QtWidgets.QHBoxLayout()
        points_layout.addWidget(QtWidgets.QLabel("Punti:"))
        points_layout.addWidget(points_edit)

        layout.addLayout(price_layout)
        layout.addLayout(points_layout)

        def save_changes():
            try:
                product['ingredienti'] = [ingredients_list.item(i).text() for i in range(ingredients_list.count())]
                product['prezzo'] = float(price_edit.text().replace(',', '.'))
                product['punti'] = int(points_edit.text())
                self.magazzino[category] = products
                self.save_magazzino()
                dialog.accept()
            except ValueError:
                QtWidgets.QMessageBox.warning(dialog, "Errore", "Prezzo o punti non validi.")

        save_btn = QtWidgets.QPushButton("Salva")
        save_btn.clicked.connect(save_changes)
        layout.addWidget(save_btn)

        cancel_btn = QtWidgets.QPushButton("Annulla")
        cancel_btn.clicked.connect(dialog.reject)
        layout.addWidget(cancel_btn)

        dialog.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaProdotti()
    window.show()
    sys.exit(app.exec())
