import pandas as pd

# Carica il dataset
df = pd.read_csv('stops.csv')

# Rimuove tutte le righe con valori nulli
df_cleaned = df.dropna()

# Salva il dataset pulito in un nuovo file
df_cleaned.to_csv('stops_cleaned.csv', index=False)

print(f"Righe originali: {len(df)}")
print(f"Righe dopo la pulizia: {len(df_cleaned)}")
