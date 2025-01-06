import json
from PySide6 import QtCore, QtWidgets, QtGui


class VisualizzaFeedback(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizza Feedback")
        self.setGeometry(100, 100, 400, 300)  # Puoi modificare le dimensioni
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Etichetta per la media dei voti
        self.media_label = QtWidgets.QLabel("Media dei Voti: Caricamento...", self)
        self.media_label.setAlignment(QtCore.Qt.AlignCenter)
        self.media_label.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(self.media_label)

        # Carica i voti e calcola la media
        self.carica_e_calcola_media()

        self.setLayout(layout)

    def carica_e_calcola_media(self):
        """Carica i voti dal file JSON e calcola la media."""
        try:
            # Controlla se il file esiste
            with open("feedback.json", "r") as file:
                feedback_data = json.load(file)

            if feedback_data:
                voti = [entry["voto"] for entry in feedback_data]
                if voti:
                    media = sum(voti) / len(voti)
                    self.media_label.setText(f"Media dei Voti: {media:.2f}")
                else:
                    self.media_label.setText("Nessun voto registrato.")
            else:
                self.media_label.setText("Nessun voto registrato.")

        except FileNotFoundError:
            self.media_label.setText("Il file dei feedback non esiste.")
        except json.JSONDecodeError:
            self.media_label.setText("Errore nel formato del file JSON.")
        except Exception as e:
            self.media_label.setText(f"Errore nel caricamento dei voti: {str(e)}")
