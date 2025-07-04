import pandas as pd

def estrai_valori_univoci_make(percorso_file):
    # Legge il file Excel
    df = pd.read_excel(percorso_file)
    
    # Controlla che la colonna "Make" esista
    if "Make" not in df.columns:
        raise ValueError("La colonna 'Make' non è presente nel file Excel.")

    # Estrae i valori univoci, rimuovendo eventuali NaN
    valori_univoci = df["Make"].dropna().unique()
    
    # Converte in lista e la restituisce
    return list(valori_univoci)

# Esempio d'uso
if __name__ == "__main__":
    file_excel = "dati.xlsx"  # Sostituisci con il percorso corretto
    lista_make = estrai_valori_univoci_make(file_excel)
    print(lista_make)
