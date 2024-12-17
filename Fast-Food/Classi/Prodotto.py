import json


class Prodotto:
    def __init__(self, nome, categoria, ingredienti, prezzo, punti, quantita):
        self.nome = nome
        self.categoria = categoria
        self.ingredienti = ingredienti
        self.prezzo = prezzo
        self.punti = punti
        self.quantita = quantita

    @staticmethod
    def leggi_da_magazzino(file_path, categoria):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                magazzino = json.load(file)
                prodotti_categoria = magazzino.get(categoria, [])

                lista_prodotti = []
                for prodotto in prodotti_categoria:
                    nome = prodotto.get("nome", "N/A")
                    ingredienti = prodotto.get("ingredienti", [])
                    prezzo = prodotto.get("prezzo", 0.0)
                    punti = prodotto.get("punti", 0)
                    quantita = prodotto.get("quantita'", 0)  # Preleva dal file o usa 0 come predefinito

                    prodotto_obj = Prodotto(
                        nome=nome,
                        categoria=categoria,
                        ingredienti=ingredienti,
                        prezzo=prezzo,
                        punti=punti,
                        quantita=quantita
                    )
                    lista_prodotti.append(prodotto_obj)

                return lista_prodotti
        except FileNotFoundError:
            print(f"Errore: Il file {file_path} non esiste.")
        except json.JSONDecodeError:
            print(f"Errore: Il file {file_path} non è un JSON valido.")

    @staticmethod
    def leggi_panini_da_magazzino(file_path):
        return Prodotto.leggi_da_magazzino(file_path, "panini")

    @staticmethod
    def leggi_contorni_da_magazzino(file_path):
        return Prodotto.leggi_da_magazzino(file_path, "contorni")

    @staticmethod
    def leggi_bevande_da_magazzino(file_path):
        return Prodotto.leggi_da_magazzino(file_path, "bevande")

    @staticmethod
    def leggi_dolci_da_magazzino(file_path):
        return Prodotto.leggi_da_magazzino(file_path, "dolci")
