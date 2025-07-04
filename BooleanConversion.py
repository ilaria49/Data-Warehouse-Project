import pandas as pd

# Caricamento del CSV
df = pd.read_csv(r'C:\Users\Hp\Desktop\Traffic_Violations.csv', low_memory=False)

# Lista delle colonne da convertire
yes_no_columns = [
    "Accident", "Belts", "Personal Injury", "Property Damage", "Fatal",
    "Commercial License", "HAZMAT", "Commercial Vehicle", "Alcohol", "Work Zone"
]

# Controllo dei valori non conformi
for col in yes_no_columns:
    unique_values = df[col].dropna().unique()
    invalid_values = [v for v in unique_values if v not in ['Yes', 'No']]
    if invalid_values:
        print(f"ATTENZIONE: colonna '{col}' (indice {df.columns.get_loc(col)}), valori non conformi trovati: {invalid_values}")

# Conversione da 'Yes'/'No' a 1/0
df[yes_no_columns] = df[yes_no_columns].replace({'Yes': 1, 'No': 0})
df[yes_no_columns] = df[yes_no_columns].infer_objects(copy=False)

# Salva il risultato
df.to_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', index=False)

print("Conversione completata: 'Yes' -> 1, 'No' -> 0 (dove possibile).")
