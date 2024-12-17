import unittest
from unittest.mock import patch
from Classi.Dipendente import Dipendente
import json
from Gestori.GestoreJSON import GestoreJSON

class TestDipendente(unittest.TestCase):

    @patch("builtins.print")
    @patch("Gestori.GestoreJSON.GestoreJSON.leggi_ordini")
    def test_visualizza_lista_ordini_clienti(self, mock_leggi_ordini, mock_print):
        mock_ordini = [
            {
                "codice_ordine": "ORD123",
                "data": "2024-01-01 10:00:00",
                "stato_ordine": "In Esecuzione",
                "prodotti": [
                    {"nome": "Panino", "tipo": "Cibo", "prezzo": 5.0, "punti": 10},
                    {"nome": "Coca-Cola", "tipo": "Bevanda", "prezzo": 2.5, "punti": 5}
                ],
                "totale": {"prezzo": 7.5, "punti": 15}
            }
        ]

        mock_leggi_ordini.return_value = mock_ordini

        Dipendente.visualizza_lista_ordini_clienti()

        mock_leggi_ordini.assert_called_once()

        mock_print.assert_any_call("\n--- Lista Ordini Clienti ---")
        mock_print.assert_any_call("Codice Ordine: ORD123")
        mock_print.assert_any_call("Data: 2024-01-01 10:00:00")
        mock_print.assert_any_call("Stato: In Esecuzione")
        mock_print.assert_any_call("Prodotti:")
        mock_print.assert_any_call("  - Panino (Cibo): €5.0 - 10 punti")
        mock_print.assert_any_call("  - Coca-Cola (Bevanda): €2.5 - 5 punti")
        mock_print.assert_any_call("Totale Prezzo: €7.5")
        mock_print.assert_any_call("Totale Punti: 15")
        mock_print.assert_any_call("------------------------------")

    @patch("builtins.print")
    @patch("Gestori.GestoreJSON.GestoreJSON.leggi_ordini")
    @patch("Gestori.GestoreJSON.GestoreJSON.salva_ordine_totale")
    def test_conferma_ordine_pronto(self, mock_salva_ordine_totale, mock_leggi_ordini, mock_print):
        mock_ordini = [
            {
                "codice_ordine": "ORD123",
                "data": "2024-01-01 10:00:00",
                "stato_ordine": "In Esecuzione",
                "prodotti": [
                    {"nome": "Panino", "tipo": "Cibo", "prezzo": 5.0, "punti": 10},
                    {"nome": "Coca-Cola", "tipo": "Bevanda", "prezzo": 2.5, "punti": 5}
                ],
                "totale": {"prezzo": 7.5, "punti": 15}
            }
        ]

        mock_leggi_ordini.return_value = mock_ordini

        Dipendente.conferma_ordine_pronto("ORD123")

        mock_leggi_ordini.assert_called_once()

        mock_salva_ordine_totale.assert_called_once_with([])

        mock_print.assert_called_with("Ordine con codice ORD123 confermato e rimosso.")

    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_accedi(self, mock_open, mock_print):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([
            {
                "username": "dipendente1",
                "password": "password123",
                "nome": "Mario",
                "cognome": "Rossi"
            }
        ])

        risultato = Dipendente.accedi("dipendente1", "password123")
        self.assertIsNotNone(risultato)
        self.assertEqual(risultato["nome"], "Mario")
        self.assertEqual(risultato["username"], "dipendente1")

        risultato = Dipendente.accedi("dipendente1", "wrongpassword")
        self.assertFalse(risultato)
        mock_print.assert_not_called()

    @patch("builtins.print")
    @patch.object(GestoreJSON, "load_magazzino")
    def test_visualizza_scorte_magazzino(self, mock_load_magazzino, mock_print):
        mock_load_magazzino.return_value = {
            "panini": [
                {"nome": "Veggie Burger", "quantita": 5, "prezzo": 6.0},
                {"nome": "Chicken Sandwich", "quantita": 15, "prezzo": 7.0}
            ],
            "bevande": [
                {"nome": "Coca-Cola", "quantita": 2, "prezzo": 2.0}
            ]
        }

        Dipendente.visualizza_scorte_magazzino()

        mock_print.assert_any_call("\n--- Scorte Magazzino ---")
        mock_print.assert_any_call("\nCategoria: panini")
        mock_print.assert_any_call("  - Veggie Burger: Quantità 5, Prezzo €6.0")
        mock_print.assert_any_call("  - Chicken Sandwich: Quantità 15, Prezzo €7.0")
        mock_print.assert_any_call("\nCategoria: bevande")
        mock_print.assert_any_call("  - Coca-Cola: Quantità 2, Prezzo €2.0")

    @patch("builtins.print")
    @patch.object(GestoreJSON, "load_magazzino")
    @patch.object(GestoreJSON, "save_magazzino")
    def test_aggiungi_scorte(self, mock_save_magazzino, mock_load_magazzino, mock_print):
        magazzino_mock = {
            "panini": [
                {"nome": "Veggie Burger", "quantita'": 5},
                {"nome": "Chicken Sandwich", "quantita'": 15}
            ],
            "bevande": [
                {"nome": "Coca-Cola", "quantita'": 2}
            ]
        }
        mock_load_magazzino.return_value = magazzino_mock

        Dipendente.aggiungi_scorte()

        mock_save_magazzino.assert_called_once()
        updated_magazzino = mock_save_magazzino.call_args[0][0]
        self.assertEqual(updated_magazzino["panini"][0]["quantita'"], 100)  # Veggie Burger
        self.assertEqual(updated_magazzino["bevande"][0]["quantita'"], 100)  # Coca-Cola
        self.assertEqual(updated_magazzino["panini"][1]["quantita'"], 15)   # Chicken Sandwich rimane invariato

        mock_print.assert_any_call("Il prodotto 'Veggie Burger' è stato rifornito a 100 unità.")
        mock_print.assert_any_call("Il prodotto 'Coca-Cola' è stato rifornito a 100 unità.")
        mock_print.assert_any_call("Scorte aggiornate con successo.")

if __name__ == "__main__":
    unittest.main()
