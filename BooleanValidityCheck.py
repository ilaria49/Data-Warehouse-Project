import pandas as pd
import numpy as np
from datetime import datetime

# Carica il dataset
df = pd.read_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', dtype={26: str})

# Lista delle colonne da convertire
yes_no_columns = [
    "Accident", "Belts", "Personal Injury", "Property Damage", "Fatal",
    "Commercial License", "HAZMAT", "Commercial Vehicle", "Alcohol", "Work Zone"
]

# Controllo e rimozione dei valori non conformi
for col in yes_no_columns:
    unique_values = df[col].dropna().unique()
    invalid_values = [v for v in unique_values if v not in ['Yes', 'No']]
    if invalid_values:
        print(f"ATTENZIONE: colonna '{col}' (indice {df.columns.get_loc(col)}), valori non conformi trovati: {invalid_values}")
        # Elimina le righe con valori non conformi
        df = df[~df[col].isin(invalid_values)]

# Conversione da 'Yes'/'No' a 1/0
df[yes_no_columns] = df[yes_no_columns].replace({'Yes': 1, 'No': 0})
df[yes_no_columns] = df[yes_no_columns].infer_objects(copy=False)

# Rimozione delle colonne non desiderate
columns_to_drop = ["Latitude", "Longitude", "Geolocation", "Contributed To Accidents"]
df = df.drop(columns=columns_to_drop, errors='ignore')  # errors='ignore' nel caso non esistano

# Salva il risultato
df.to_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', index=False)

print("Conversione e pulizia completate. Dati salvati.")
