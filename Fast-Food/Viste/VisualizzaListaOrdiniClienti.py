import sys
import json
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QScrollArea
from Gestori.GestoreJSON import GestoreJSON


class VisualizzaListaOrdiniClienti(QWidget):
    def __init__(self):
        super().__init__()
        self.gestore_json = GestoreJSON()
        self.ordini = self.gestore_json.leggi_ordini()

        # Filtra gli ordini con stato diverso da "Confermato"
        self.ordini_filtrati = [ordine for ordine in self.ordini if ordine["stato_ordine"] != "Confermato"]

        if not self.ordini_filtrati:
            QMessageBox.information(self, "Nessun Ordine", "Non ci sono ordini da visualizzare.")
            self.deleteLater()

        else:
            self.inizializza_interfaccia_cliente()

    def inizializza_interfaccia_cliente(self):
        self.setWindowTitle("Fast-Food - Lista Ordini")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: white;")

        # Creazione dello scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Contenitore per tutti gli ordini
        contenitore = QWidget()
        layout_principale = QVBoxLayout(contenitore)

        intestazione = QLabel("Visualizza Lista Ordini Clienti")
        intestazione.setAlignment(QtCore.Qt.AlignCenter)
        intestazione.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        layout_principale.addWidget(intestazione)

        for ordine in self.ordini_filtrati:
            layout_ordine = QVBoxLayout()
            layout_ordine.setSpacing(10)

            # Mostra la data dell'ordine
            info_ordine = QLabel(f"Data Ordine: {ordine['data']} | Stato: {ordine['stato_ordine']} "
                                  f"| Codice: {ordine['codice_ordine']}")
            info_ordine.setStyleSheet("font-weight: bold; font-size: 14px; color: #0055ff;")
            layout_ordine.addWidget(info_ordine)

            # Mostra i prodotti
            for prodotto in ordine["prodotti"]:
                nome_prodotto = prodotto["nome"]
                prezzo_prodotto = prodotto["prezzo"]
                etichetta_prodotto = QLabel(f"- {nome_prodotto} (Prezzo: €{prezzo_prodotto:.2f})")
                etichetta_prodotto.setStyleSheet("color: #444444;")
                layout_ordine.addWidget(etichetta_prodotto)

            # Mostra il totale
            totale_ordine = QLabel(
                f"Totale: €{ordine['totale']['prezzo']:.2f} - Punti: {ordine['totale']['punti']}")
            totale_ordine.setStyleSheet("font-weight: bold; font-size: 12px; color: #333333;")
            layout_ordine.addWidget(totale_ordine)

            # Aggiungi pulsante per confermare ordine
            pulsante_conferma = QPushButton("Conferma Ordine Pronto")
            pulsante_conferma.setStyleSheet(
                "background-color: #4CAF50; color: black; font-weight: bold; padding: 5px;")

            pulsante_conferma.clicked.connect(self.crea_callback_conferma(ordine["codice_ordine"]))
            layout_ordine.addWidget(pulsante_conferma)

            layout_principale.addLayout(layout_ordine)

        contenitore.setLayout(layout_principale)
        scroll_area.setWidget(contenitore)

        # Layout principale del widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def conferma_ordine_pronto(self, codice_ordine):
        #Conferma un ordine, cambiando il suo stato a 'Confermato'.

        try:
            # Carica gli ordini dal file JSON
            with open(self.gestore_json.ordini_file, "r", encoding="utf-8") as file:
                ordini = json.load(file)

            if not isinstance(ordini, list):
                raise ValueError("Il file JSON non contiene un elenco di ordini.")

            # Trova l'ordine corrispondente
            ordine_trovato = False
            for ordine in ordini:
                if not isinstance(ordine, dict):
                    continue  # Ignora elementi non validi
                if ordine.get("codice_ordine") == codice_ordine:
                    ordine["stato_ordine"] = "Confermato"
                    ordine_trovato = True
                    break

            if not ordine_trovato:
                QMessageBox.warning(self, "Errore", "Ordine non trovato.")
                return

            # Salva il file aggiornato
            with open(self.gestore_json.ordini_file, "w", encoding="utf-8") as file:
                json.dump(ordini, file, indent=4)

            # Messaggio di conferma con testo nero
            QtWidgets.QMessageBox.information(
                self,
                "Confermato",
                f"<p style='color: black;'>L'ordine del cliente è stato confermato con successo.</p>"
            )

            # Chiudi l'interfaccia corrente e crea una nuova finestra aggiornata
            self.close()
            nuova_finestra = VisualizzaListaOrdiniClienti()
            nuova_finestra.show()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Errore", f"Errore durante la conferma dell'ordine: {str(e)}")

    def crea_callback_conferma(self, codice_ordine):
        def callback():
            self.conferma_ordine_pronto(codice_ordine)

        return callback


if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = VisualizzaListaOrdiniClienti()
    finestra.show()
    sys.exit(app.exec())
