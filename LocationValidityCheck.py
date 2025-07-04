import pandas as pd

input_file = 'cleaned.xlsx'
df = pd.read_excel(input_file)

def is_numeric_only(val):
    if pd.isna(val):
        return False
    val = str(val).strip()
    return val.isdigit()
valid_mask = ~df['Location'].apply(is_numeric_only)
df_valid = df[valid_mask]
totale = len(df)
validi = len(df_valid)
percentuale_validi = (validi / totale) * 100 if totale > 0 else 0
df_valid.to_excel('location_filtrata.xlsx', index=False)

# Stampa i risultati
print(f"Righe totali: {totale}")
print(f"Righe con 'Location' valida: {validi}")
print(f"Percentuale di dati validi: {percentuale_validi:.2f}%")
print("File salvato come 'location_filtrata.xlsx'")
