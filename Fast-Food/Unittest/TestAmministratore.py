import unittest
from unittest.mock import MagicMock, patch
from Classi.Amministratore import Amministratore


class TestAmministratore(unittest.TestCase):
    def setUp(self):
        self.admin = Amministratore("Mario", "Rossi", "mario.rossi@example.com", "password123", "1234567890", "admin1",
                                    "A001")
        self.admin.gestore_json = MagicMock()

    def test_aggiungi_dipendente(self):
        self.admin.aggiungi_dipendente("Luca", "Bianchi", "1990-01-01", "0987654321", "luca.bianchi@example.com",
                                       "luca.bianchi", "pass456")

        self.admin.gestore_json.aggiungi_dipendente.assert_called_with({
            "nome": "Luca",
            "cognome": "Bianchi",
            "data_di_nascita": "1990-01-01",
            "telefono": "0987654321",
            "email": "luca.bianchi@example.com",
            "username": "luca.bianchi",
            "password": "pass456"
        })

    def test_modifica_dipendente(self):
        nuovi_dati = {
            "nome": "Luca",
            "cognome": "Bianchi",
            "data_di_nascita": "1990-01-01",
            "telefono": "1111111111",
            "email": "luca.bianchi@example.com",
            "username": "luca.bianchi",
            "password": "newpass123"
        }
        self.admin.modifica_dipendente("luca.bianchi@example.com", nuovi_dati)

        self.admin.gestore_json.modifica_dipendente.assert_called_with("luca.bianchi@example.com", nuovi_dati)

    def test_elimina_dipendente(self):
        self.admin.elimina_dipendente("luca.bianchi@example.com")

        self.admin.gestore_json.elimina_dipendente.assert_called_with("luca.bianchi@example.com")

    def test_aggiungi_prodotto(self):
        self.admin.aggiungi_prodotto("panini", "Veggie Burger", ["pane", "verdure", "formaggio"], 5.5, 20, 10)

        self.admin.gestore_json.aggiungi_prodotto.assert_called_with(
            "panini", "Veggie Burger", ["pane", "verdure", "formaggio"], 5.5, 20, 10
        )

    def test_modifica_prodotto(self):
        nuovi_dati = {
            "prezzo": 6.0,
            "quantita'": 15
        }
        self.admin.modifica_prodotto("panini", "Veggie Burger", nuovi_dati)

        self.admin.gestore_json.modifica_prodotto.assert_called_with("panini", "Veggie Burger", nuovi_dati)

    def test_elimina_prodotto(self):
        self.admin.elimina_prodotto("panini", "Veggie Burger")

        self.admin.gestore_json.elimina_prodotto.assert_called_with("panini", "Veggie Burger")

    @patch("builtins.print")
    def test_visualizza_dipendenti(self, mock_print):
        self.admin.gestore_json.load_dipendenti.return_value = [
            {"nome": "Luca", "cognome": "Bianchi", "email": "luca.bianchi@example.com", "telefono": "123456789"},
            {"nome": "Maria", "cognome": "Verdi", "email": "maria.verdi@example.com", "telefono": "987654321"}
        ]

        self.admin.visualizza_dipendenti()

        mock_print.assert_any_call("\n--- Elenco Dipendenti ---")
        mock_print.assert_any_call("1. Luca Bianchi - Email: luca.bianchi@example.com - Telefono: 123456789")
        mock_print.assert_any_call("2. Maria Verdi - Email: maria.verdi@example.com - Telefono: 987654321")

    @patch("builtins.print")
    def test_visualizza_feedback(self, mock_print):
        self.admin.gestore_json.leggi_feedback.return_value = [
            {"voto": 5},
            {"voto": 4},
            {"voto": 3}
        ]

        self.admin.visualizza_feedback()

        mock_print.assert_any_call("\n--- Feedback ricevuti ---")
        mock_print.assert_any_call("1. 5 stelle")
        mock_print.assert_any_call("2. 4 stelle")
        mock_print.assert_any_call("3. 3 stelle")

if __name__ == "__main__":
    unittest.main()