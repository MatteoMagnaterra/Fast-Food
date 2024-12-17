import sys
import json
from PySide6 import QtCore, QtWidgets, QtGui
from Viste.VisualizzaProdottiClienti import VisualizzaProdottiCliente
from Viste.VisualizzaAccountCliente import VisualizzaAccountCliente
from Viste.EffettuaOrdine import EffettuaOrdine


class HomepageCliente(QtWidgets.QWidget):
    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente #salva l'istanza del cliente
        self.setWindowTitle("Fast-Food - Homepage Cliente")
        self.setGeometry(100, 100, 400, 500)
        self.voto_confermato = False  # Per verificare se il feedback è stato confermato
        self.voto_selezionato = 0  # Numero di stelle selezionate
        self.file_feedback = "feedback.json"
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Titolo
        title_label = QtWidgets.QLabel(f"Ciao, {self.cliente.nome}", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        layout.addWidget(title_label)

        # Bottoni
        button_layout = QtWidgets.QHBoxLayout()
        self.order_button = QtWidgets.QPushButton("Effettua Ordine", self)
        self.products_button = QtWidgets.QPushButton("Visualizza Prodotti", self)
        self.account_button = QtWidgets.QPushButton("Visualizza Account", self)

        button_layout.addWidget(self.order_button)
        button_layout.addWidget(self.products_button)
        button_layout.addWidget(self.account_button)

        layout.addWidget(self.order_button)
        layout.addWidget(self.products_button)
        layout.addWidget(self.account_button)

        self.account_button.clicked.connect(self.open_account_window)
        self.products_button.clicked.connect(self.open_products_window)
        self.order_button.clicked.connect(self.open_orders_window)

        # Sezione di feedback con stelle
        stars_layout = QtWidgets.QHBoxLayout()
        self.stars = []

        for i in range(1, 6):
            star_label = QtWidgets.QLabel("☆", self)
            star_label.setAlignment(QtCore.Qt.AlignCenter)
            star_label.setFont(QtGui.QFont("Arial", 24))
            star_label.mousePressEvent = self.create_star_click_handler(i)
            stars_layout.addWidget(star_label)
            self.stars.append(star_label)

        layout.addLayout(stars_layout)

        # Pulsante di conferma
        self.confirm_button = QtWidgets.QPushButton("Conferma Voto", self)
        self.confirm_button.clicked.connect(self.conferma_voto)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)


    def create_star_click_handler(self, index):
        #Crea un gestore di eventi per cliccare sulle stelle

        def handler(event):
            if not self.voto_confermato:  # Permette di selezionare solo se non confermato
                self.voto_selezionato = index
                self.update_star_display()

        return handler


    def update_star_display(self):
        """Aggiorna il colore delle stelle in base al voto selezionato."""
        for i, star_label in enumerate(self.stars, start=1):
            if i <= self.voto_selezionato:
                star_label.setText("★")  # Stella piena
                star_label.setStyleSheet("color: gold;")
            else:
                star_label.setText("☆")  # Stella vuota
                star_label.setStyleSheet("color: black;")

    def conferma_voto(self):
        """Conferma il voto selezionato, salva il voto in un file JSON e disabilita ulteriori modifiche."""
        if self.voto_selezionato > 0:  # Solo se è stato selezionato un voto
            self.voto_confermato = True
            self.salva_feedback(self.voto_selezionato)  # Salva il voto nel file JSON

            # Disabilita il pulsante e le stelle
            self.confirm_button.setEnabled(False)
            self.confirm_button.setText("Voto Confermato")
            for star_label in self.stars:
                star_label.setEnabled(False)
        else:
            QtWidgets.QMessageBox.warning(self, "Attenzione", "Seleziona almeno una stella prima di confermare.")

    def salva_feedback(self, voto):
        """Salva il voto in un file JSON."""
        try:
            # Carica i dati esistenti se il file esiste
            try:
                with open(self.file_feedback, "r") as file:
                    feedback_data = json.load(file)
            except FileNotFoundError:
                feedback_data = []  # Nessun feedback precedente

            # Aggiungi il nuovo voto
            feedback_data.append({"voto": voto})

            # Salva i dati aggiornati nel file
            with open(self.file_feedback, "w") as file:
                json.dump(feedback_data, file, indent=4)
            print(f"Voto {voto} salvato con successo in {self.file_feedback}.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Errore", f"Impossibile salvare il voto: {str(e)}")

    def open_account_window(self):
        # Passa l'istanza dell'amministratore alla finestra VisualizzaAccount
        self.account_window = VisualizzaAccountCliente(self.cliente)
        self.account_window.show()

    def open_products_window(self):
        self.products_window = VisualizzaProdottiCliente()
        self.products_window.show()

    def open_orders_window(self):
        self.products_window = EffettuaOrdine()
        self.products_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomepageCliente()
    window.show()
    sys.exit(app.exec())