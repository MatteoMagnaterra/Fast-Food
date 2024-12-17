import sys
from PySide6 import QtCore, QtWidgets, QtGui
from Gestori.GestoreJSON import GestoreJSON
from Viste.AggiungiDipendente import AggiungiDipendente


class VisualizzaDipendenti(QtWidgets.QWidget):
    def __init__(self, amministratore = None):
        super().__init__()
        self.setWindowTitle("Fast-Food - Visualizza Dettagli Dipendenti")
        self.setGeometry(150, 150, 800, 600)
        self.dipendenti_widgets = []  # Lista per mantenere i riferimenti ai widget
        self.gestore_json = GestoreJSON()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Titolo della finestra
        title_label = QtWidgets.QLabel("Visualizza Dettagli Dipendenti", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 18))
        layout.addWidget(title_label)

        # Pulsante "Aggiungi Dipendente"
        add_dipendente_button = QtWidgets.QPushButton("Aggiungi Dipendente", self)
        add_dipendente_button.clicked.connect(self.open_add_dipendente_dialog)
        layout.addWidget(add_dipendente_button)

        # Scroll Area per i dipendenti
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Contenitore per i widget dei dipendenti
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)

        # Caricare i dipendenti dal JSON
        dipendenti = self.gestore_json.load_dipendenti()

        # Iterare sui dipendenti e aggiungerli al layout
        if dipendenti:
            for idx, dipendente in enumerate(dipendenti):
                dipendente_widget = self.crea_dipendente_widget(dipendente, idx + 1)
                self.scroll_layout.addWidget(dipendente_widget)
                self.dipendenti_widgets.append(dipendente_widget)  # Mantieni un riferimento al widget
        else:
            QtWidgets.QMessageBox.information(self, "Nessun Dipendente", "Non ci sono dipendenti da visualizzare.")

        self.scroll_content.setLayout(self.scroll_layout)
        scroll_area.setWidget(self.scroll_content)

        # Aggiungere l'area di scorrimento al layout principale
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def crea_dipendente_widget(self, dipendente, numero):
        """Crea un widget per visualizzare i dati di un singolo dipendente."""
        widget = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(widget)

        # Dati del dipendente
        nome_edit = QtWidgets.QLineEdit(dipendente["nome"])
        cognome_edit = QtWidgets.QLineEdit(dipendente["cognome"])
        data_di_nascita_edit = QtWidgets.QLineEdit(dipendente["data_di_nascita"])
        telefono_edit = QtWidgets.QLineEdit(dipendente["telefono"])
        email_edit = QtWidgets.QLineEdit(dipendente["email"])
        username_edit = QtWidgets.QLineEdit(dipendente["username"])
        password_edit = QtWidgets.QLineEdit(dipendente["password"])

        # Rendere i campi non modificabili per la visualizzazione iniziale
        for field in [nome_edit, cognome_edit, data_di_nascita_edit, telefono_edit, email_edit, username_edit, password_edit]:
            field.setDisabled(True)

        # Layout per i dati del dipendente
        info_layout = QtWidgets.QFormLayout()
        info_layout.addRow(f"Dipendente {numero}", QtWidgets.QLabel())
        info_layout.addRow("Nome:", nome_edit)
        info_layout.addRow("Cognome:", cognome_edit)
        info_layout.addRow("Data di Nascita:", data_di_nascita_edit)
        info_layout.addRow("Telefono:", telefono_edit)
        info_layout.addRow("Email:", email_edit)
        info_layout.addRow("Username:", username_edit)
        info_layout.addRow("Password:", password_edit)

        h_layout.addLayout(info_layout)

        # Pulsante per Modifica Account
        modifica_button = QtWidgets.QPushButton("Modifica Account")
        modifica_button.setIcon(QtGui.QIcon.fromTheme("edit"))
        modifica_button.setIconSize(QtCore.QSize(32, 32))
        modifica_button.clicked.connect(
            lambda: self.modifica_dipendente(
                dipendente,
                nome_edit,
                cognome_edit,
                data_di_nascita_edit,
                telefono_edit,
                email_edit,
                username_edit,
                password_edit,
                modifica_button
            )
        )
        h_layout.addWidget(modifica_button)

        # Pulsante per Eliminare Account
        elimina_button = QtWidgets.QPushButton("Elimina Account")
        elimina_button.setIcon(QtGui.QIcon.fromTheme("delete"))
        elimina_button.setIconSize(QtCore.QSize(32, 32))
        elimina_button.clicked.connect(lambda: self.elimina_dipendente(dipendente))
        h_layout.addWidget(elimina_button)

        return widget

    def modifica_dipendente(self, dipendente, nome_edit, cognome_edit, data_di_nascita_edit, telefono_edit, email_edit, username_edit, password_edit, modifica_button):
        """Attiva la modalità di modifica per un dipendente."""
        if not hasattr(modifica_button, 'in_modifica') or not modifica_button.in_modifica:
            # Abilita la modifica dei campi
            for widget in [nome_edit, cognome_edit, data_di_nascita_edit, telefono_edit, email_edit, username_edit, password_edit]:
                widget.setDisabled(False)

            # Cambia il testo del pulsante per riflettere la modalità di salvataggio
            modifica_button.setText("Salva Modifiche")
            modifica_button.in_modifica = True
        else:
            # Raccogli i dati modificati
            nuovi_dati = {
                "nome": nome_edit.text(),
                "cognome": cognome_edit.text(),
                "data_di_nascita": data_di_nascita_edit.text(),
                "telefono": telefono_edit.text(),
                "email": email_edit.text(),
                "username": username_edit.text(),
                "password": password_edit.text()
            }

            # Verifica che i dati siano validi prima di salvare
            if not self.gestore_json.is_valid_email(nuovi_dati["email"]):
                QtWidgets.QMessageBox.warning(self, "Errore",
                                              "L'email inserita non è valida. Inserisci un'email valida.")
                return

            if not self.gestore_json.is_unique("dipendenti", {"email": nuovi_dati["email"]},
                                          current_username=dipendente["email"]):
                QtWidgets.QMessageBox.warning(self, "Errore", "L'email è già in uso. Scegli un'altra email.")
                return

            # Controllo numero di telefono
            if not self.gestore_json.is_valid_phone_number(nuovi_dati["telefono"]):
                QtWidgets.QMessageBox.warning(self, "Errore",
                                                  "Il numero di telefono inserito non è valido. Deve contenere solo 10 cifre.")
                return

            # Aggiorna i dati del dipendente usando l'email corrente come identificatore
            self.gestore_json.modifica_dipendente( dipendente["email"], nuovi_dati)

            # Disabilita nuovamente i campi
            for widget in [nome_edit, cognome_edit, data_di_nascita_edit, telefono_edit, email_edit, username_edit, password_edit]:
                widget.setDisabled(True)

            # Cambia il testo del pulsante indietro a "Modifica Account"
            modifica_button.setText("Modifica Account")
            modifica_button.in_modifica = False

            QtWidgets.QMessageBox.information(self, "Successo",
                                              "I dati del dipendente sono stati aggiornati con successo.")

    def elimina_dipendente(self, dipendente):
        """Elimina il dipendente specificato."""
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare l'account del dipendente {dipendente['nome']} {dipendente['cognome']}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                # Elimina il dipendente dal file JSON
                self.gestore_json.elimina_dipendente(dipendente["email"])

                # Rimuovi il widget associato dall'interfaccia
                widget_to_remove = None
                for widget in self.dipendenti_widgets:
                    form_layout = widget.layout().itemAt(0).layout()
                    email_widget = form_layout.itemAt(8).widget()  # L'email è l'ottavo elemento del form layout
                    if email_widget.text() == dipendente["email"]:
                        widget_to_remove = widget
                        break

                if widget_to_remove:
                    self.scroll_layout.removeWidget(widget_to_remove)
                    widget_to_remove.deleteLater()
                    self.dipendenti_widgets.remove(widget_to_remove)

                # Mostra un messaggio di conferma
                QtWidgets.QMessageBox.information(self, "Account Eliminato",
                                                  f"Il dipendente {dipendente['nome']} {dipendente['cognome']} è stato eliminato con successo.")

            except ValueError as e:
                QtWidgets.QMessageBox.critical(self, "Errore", str(e))

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Errore", f"Si è verificato un errore imprevisto: {str(e)}")

    def reload_interface(self):
        """Ricarica la finestra per riflettere le modifiche."""
        self.close()
        self.__init__()
        self.show()

    def load_dipendenti(self):
        """Ricarica i dipendenti e aggiorna l'interfaccia."""
        # Pulisci i widget esistenti
        while self.scroll_layout.count():
            widget = self.scroll_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        self.dipendenti_widgets.clear()

        # Ricarica i dati
        dipendenti = self.gestore_json.load_dipendenti()

        if dipendenti:
            for idx, dipendente in enumerate(dipendenti):
                dipendente_widget = self.crea_dipendente_widget(dipendente, idx + 1)
                self.scroll_layout.addWidget(dipendente_widget)
                self.dipendenti_widgets.append(dipendente_widget)
        else:
            QtWidgets.QMessageBox.information(self, "Nessun Dipendente", "Non ci sono dipendenti da visualizzare.")

    def open_add_dipendente_dialog(self):
        """Apre la finestra di dialogo per aggiungere un nuovo dipendente."""
        self.feedback_window = AggiungiDipendente()
        self.feedback_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VisualizzaDipendenti()
    window.show()
    sys.exit(app.exec())