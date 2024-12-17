import unittest
from unittest.mock import MagicMock, patch
from Classi.Cliente import Cliente
from Gestori.GestoreJSON import GestoreJSON
import json

class TestCliente(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(
            nome="Mario",
            cognome="Rossi",
            email="mario.rossi@example.com",
            password="password123",
            telefono="1234567890",
            username="mrossi",
        )
        self.gestore_json_mock = MagicMock(spec=GestoreJSON)
        self.gestore_json_mock.salva_feedback = MagicMock()
        self.gestore_json_mock.load_magazzino = MagicMock()
        self.gestore_json_mock.load_data = MagicMock()
        self.cliente.gestore_json = self.gestore_json_mock

    def test_crea_cliente(self):
        self.assertEqual(self.cliente.nome, "Mario")
        self.assertEqual(self.cliente.cognome, "Rossi")
        self.assertEqual(self.cliente.email, "mario.rossi@example.com")
        self.assertEqual(self.cliente.password, "password123")
        self.assertEqual(self.cliente.telefono, "1234567890")
        self.assertEqual(self.cliente.username, "mrossi")

    @patch("builtins.print")
    def test_visualizza_account(self, mock_print):
        self.gestore_json_mock.load_data.return_value = {
            "clienti": [
                {
                    "nome": "Mario",
                    "cognome": "Rossi",
                    "email": "mario.rossi@example.com",
                    "password": "password123",
                    "telefono": "1234567890",
                    "username": "mrossi"
                }
            ]
        }
        risultato = self.cliente.visualizza_account()
        self.assertIsNotNone(risultato)
        self.assertEqual(risultato["nome"], "Mario")
        self.assertEqual(risultato["cognome"], "Rossi")
        self.assertEqual(risultato["email"], "mario.rossi@example.com")
        self.assertEqual(risultato["password"], "password123")
        self.assertEqual(risultato["telefono"], "1234567890")
        self.assertEqual(risultato["username"], "mrossi")

    def test_modifica_account(self):
        nuovi_dati = {
            "nome": "Luigi",
            "cognome": "Bianchi",
            "email": "luigi.bianchi@example.com",
            "password": "newpassword123",
            "telefono": "0987654321",
            "username": "lbianchi"
        }

        self.gestore_json_mock.is_unique.return_value = True

        risultato = self.cliente.modifica_account(nuovi_dati)

        self.assertTrue(risultato)
        self.assertEqual(self.cliente.nome, "Luigi")
        self.assertEqual(self.cliente.cognome, "Bianchi")
        self.assertEqual(self.cliente.email, "luigi.bianchi@example.com")
        self.assertEqual(self.cliente.password, "newpassword123")
        self.assertEqual(self.cliente.telefono, "0987654321")
        self.assertEqual(self.cliente.username, "lbianchi")

        self.gestore_json_mock.modifica_dati.assert_called_once_with("clienti", "mrossi", nuovi_dati)

    def test_elimina_account(self):
        self.cliente.elimina_account()
        self.gestore_json_mock.delete_data_cliente.assert_called_once_with("mrossi", "password123")

    @patch("builtins.input", side_effect=["Chicken Sandwich", "1", "fine", "sì"])
    @patch("builtins.print")
    def test_effettua_ordine(self, mock_print, mock_input):
        magazzino_mock = {
            "panini": [
                {
                    "nome": "Chicken Sandwich",
                    "prezzo": 7.0,
                    "punti": 15,
                    "quantita": 10
                }
            ]
        }

        self.gestore_json_mock.load_magazzino.return_value = magazzino_mock

        ordine = self.cliente.effettua_ordine()

        self.assertIsNotNone(ordine)
        self.assertEqual(ordine["stato_ordine"], "In Esecuzione")
        self.assertEqual(len(ordine["prodotti"]), 1)
        self.assertEqual(ordine["prodotti"][0]["nome"], "Chicken Sandwich")
        self.assertEqual(ordine["prodotti"][0]["quantita"], 1)
        self.assertEqual(ordine["prodotti"][0]["punti"], 15)
        self.assertEqual(ordine["totale"]["prezzo"], 7.0)
        self.assertEqual(ordine["totale"]["punti"], 15)

        self.gestore_json_mock.salva_ordine.assert_called_once_with(ordine)
        self.gestore_json_mock.save_magazzino.assert_called_once()

    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_accedi(self, mock_open, mock_print):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
            "clienti": [
                {
                    "nome": "Mario",
                    "cognome": "Rossi",
                    "email": "mario.rossi@example.com",
                    "password": "password123",
                    "telefono": "1234567890",
                    "username": "mrossi"
                }
            ]
        })

        cliente = Cliente.accedi("mrossi", "password123")
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["nome"], "Mario")
        self.assertEqual(cliente["username"], "mrossi")

    @patch("builtins.print")
    def test_crea_feedback(self, mock_print):
        self.gestore_json_mock.salva_feedback.return_value = None

        risultato = self.cliente.crea_feedback(5)
        self.assertTrue(risultato)
        self.gestore_json_mock.salva_feedback.assert_called_once_with(5)
        mock_print.assert_any_call("Feedback di 5 stelle salvato con successo.")

        self.gestore_json_mock.reset_mock()
        risultato = self.cliente.crea_feedback(6)
        self.assertFalse(risultato)
        self.gestore_json_mock.salva_feedback.assert_not_called()
        mock_print.assert_any_call("Errore: il voto deve essere compreso tra 1 e 5 stelle.")

    @patch("builtins.print")
    @patch.object(Cliente, "invia_email_password")
    def test_recupera_password(self, mock_invia_email, mock_print):
        self.gestore_json_mock.load_data.return_value = {
            "clienti": [
                {
                    "email": "mario.rossi@example.com",
                    "password": "password123"
                }
            ]
        }
        self.gestore_json_mock.salva_dati = MagicMock()

        risultato = self.cliente.recupera_password("mario.rossi@example.com")

        self.assertTrue(risultato)
        self.gestore_json_mock.salva_dati.assert_called_once()
        mock_invia_email.assert_called_once_with("mario.rossi@example.com", mock_invia_email.call_args[0][1])
        mock_print.assert_called_with("Una nuova password è stata inviata al tuo indirizzo email.")

    @patch("builtins.print")
    def test_visualizza_prodotti(self, mock_print):
        magazzino_mock = {
            "panini": [
                {
                    "nome": "Veggie Burger",
                    "prezzo": 6.0,
                    "quantita": 5,
                    "punti": 10
                }
            ]
        }
        self.cliente.visualizza_prodotti(magazzino_mock)
        mock_print.assert_any_call("\nCategoria: panini")
        mock_print.assert_any_call("- Veggie Burger: €6.0 (5 disponibili, 10 punti)")

    @patch("builtins.print")
    def test_filtra_prodotto(self, mock_print):
        magazzino_mock = {
            "panini": [
                {
                    "nome": "Veggie Burger",
                    "prezzo": 6.0,
                    "quantita": 5,
                    "ingredienti": ["verdure", "pane"]
                },
                {
                    "nome": "Chicken Sandwich",
                    "prezzo": 7.0,
                    "quantita": 10,
                    "ingredienti": ["pollo", "pane"]
                }
            ]
        }
        risultato = self.cliente.filtra_prodotto(magazzino_mock, "pollo")
        self.assertEqual(len(risultato), 1)
        self.assertEqual(risultato[0]["nome"], "Chicken Sandwich")
        mock_print.assert_any_call("Categoria: panini, Nome: Chicken Sandwich, Prezzo: €7.0, Quantità: 10")

if __name__ == "__main__":
    unittest.main()
