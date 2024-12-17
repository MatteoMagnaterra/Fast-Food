import pandas as pd
import json
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funzione per caricare i dati da un file JSON
def load_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Funzione per preparare i DataFrame dai dati caricati
def prepare_dataframe(data):
    # Crezione di due liste: una per i dati degli ordini e una per i prodotti
    orders_data = []
    products_data = []
    for entry in data:
        # Calcola il valore totale dell'ordine sommando i prezzi dei prodotti
        total_order_price = sum(product['prezzo'] for product in entry['prodotti'])
        orders_data.append({
            'date': pd.to_datetime(entry['data']), #Serve a convertire la data in formato datetime
            'order_value': total_order_price #Valore totale dell'ordine
        })
        for product in entry['prodotti']:
            # Aggiunge i dettagli dei prodotti a una lista separata
            products_data.append({
                'date': pd.to_datetime(entry['data']),
                'product_name': product['nome'],
                'quantity': product.get('quantita', 1)
            })
    return pd.DataFrame(orders_data), pd.DataFrame(products_data)

# Aggiunge colonne per analisi temporale (annuale,mensile,annuale)
def add_date_parts(df):
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_year'] = df['date'].dt.strftime('%Y-%m')
    df['week'] = df['date'].dt.isocalendar().week
    df['week_year'] = df['date'].dt.strftime('%Y-W%V')

#Aggregazione di dati per anno,mese e settimana
def aggregate_data(df):
    aggregations = {
        'total_orders': pd.NamedAgg(column='date', aggfunc='count'),
        'total_sales': pd.NamedAgg(column='order_value', aggfunc='sum')
    }
    #Raggruppa i dati annuali,mensili e settimanali
    annual_stats = df.groupby('year').agg(**aggregations).reset_index()
    monthly_stats = df.groupby('month_year').agg(**aggregations).reset_index()
    weekly_stats = df.groupby('week_year').agg(**aggregations).reset_index()
    return annual_stats, monthly_stats, weekly_stats

#Calcola i prodotti più venduti per anno
def calculate_top_products(products_df):
    products_df['year'] = products_df['date'].dt.year # Estrae l'anno dai dati dei prodotti
    # Raggruppa i dati per anno e nome prodotto, calcolando la quantità totale
    top_products = products_df.groupby(['year', 'product_name'])['quantity'].sum().reset_index()
    # Ordina i prodotti per anno e quantità in ordine decrescente
    top_products = top_products.sort_values(['year', 'quantity'], ascending=[True, False])
    return top_products

# Creazione di un grafico all'interno di un frame Tkinter
def create_chart(frame, stats, x, y, title):
    fig, ax = plt.subplots() # Crea una figura e un asse
    stats.plot(x=x, y=y, kind='bar', ax=ax, legend=None) # Crea un grafico a barre
    ax.set_title(title) # Imposta il titolo del grafico
    ax.set_xlabel('') # Rimuove l'etichetta asse x
    ax.set_ylabel('Total Sales')  # Etichetta asse y
    chart = FigureCanvasTkAgg(fig, master=frame)  # Integra il grafico con Tkinter
    chart.draw()
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # Posiziona il grafico nel frame

# Mostra i prodotti più venduti per un anno selezionato
def display_top_products(frame, top_products, selected_year):
    # Filtra i prodotti per l'anno selezionato e prende i primi 5
    filtered_products = top_products[top_products['year'] == selected_year].head(5)

    fig, ax = plt.subplots() # Crea una nuova figura e asse
    filtered_products.plot(x='product_name', y='quantity', kind='bar', ax=ax, legend=None) # Grafico a barre
    ax.set_title(f'Top 5 Prodotti Venduti nel {selected_year}') # Titolo del grafico
    ax.set_xlabel('Prodotto') # Etichetta asse x
    ax.set_ylabel('Quantità') # asse y

    chart = FigureCanvasTkAgg(fig, master=frame) # Integra il grafico con Tkinter
    chart.draw()
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) # Posiziona il grafico nel frame

def main():
    # Carica i dati dal file
    data = load_data('Ordini.json')
    df, products_df = prepare_dataframe(data)
    add_date_parts(df) #Aggiunge colonne per ordini e prodotti
    annual_stats, monthly_stats, weekly_stats = aggregate_data(df)
    top_products = calculate_top_products(products_df)

    # Interfaccia grafica
    root = tk.Tk()
    root.title("Statistiche degli Ordini")
    tab_control = ttk.Notebook(root) #widget a schede

    #Crea schede
    annual_tab = ttk.Frame(tab_control)
    monthly_tab = ttk.Frame(tab_control)
    weekly_tab = ttk.Frame(tab_control)
    top_products_tab = ttk.Frame(tab_control)

    tab_control.add(annual_tab, text='Annuali')
    tab_control.add(monthly_tab, text='Mensili')
    tab_control.add(weekly_tab, text='Settimanali')
    tab_control.add(top_products_tab, text='Top Prodotti')

    tab_control.pack(expand=1, fill='both')

    #Crea i grafici per ogni scheda
    create_chart(annual_tab, annual_stats, 'year', 'total_sales', 'Vendite Annuali')
    create_chart(monthly_tab, monthly_stats, 'month_year', 'total_sales', 'Vendite Mensili')
    create_chart(weekly_tab, weekly_stats, 'week_year', 'total_sales', 'Vendite Settimanali')

    # Top Prodotti
    def update_top_products():
        if not year_combo.get():  # Controlla che l'anno sia selezionato
            return
        try:
            selected_year = int(year_combo.get())
            for widget in top_products_tab.winfo_children():
                widget.destroy()
            display_top_products(top_products_tab, top_products, selected_year)
        except ValueError:
            print("Errore: selezione dell'anno non valida")

    year_label = tk.Label(top_products_tab, text="Seleziona Anno:")
    year_label.pack()

    year_combo = ttk.Combobox(top_products_tab, values=top_products['year'].unique().tolist()) #Dropdown per anni
    if year_combo['values']:  # Imposta un valore predefinito se la lista non è vuota
        year_combo.current(0)
    year_combo.pack()
    year_combo.bind("<<ComboboxSelected>>", lambda e: update_top_products()) #Aggiorna il grafico alla sezione

    #Funzione per chiudere correttamente la finestra
    def on_close():
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop() #Avvis il ciclo principale di Tkinter

if __name__ == '__main__':
    main()
