import pandas as pd
from datetime import datetime

# Carica il dataset
df = pd.read_csv(r'C:\Users\Hp\Desktop\Traffic_Violations.csv', low_memory=False)

# Ottieni l'anno corrente
current_year = datetime.now().year

# Completeness: non nulli
complete_mask = df["Year"].notnull()
completeness = complete_mask.mean() * 100

# Validity: anni tra 1900 e l'anno corrente
valid_mask = df["Year"].between(1900, current_year, inclusive="both")
validity = valid_mask.mean() * 100

# Precision: valori interi
precise_mask = df["Year"].apply(lambda x: isinstance(x, int) or (isinstance(x, float) and x.is_integer()))
precision = precise_mask.mean() * 100

# Consistency: coerenti con la data della violazione (Year <= year of stop)
# Prima convertiamo 'Date Of Stop' in datetime
df["Date Of Stop"] = pd.to_datetime(df["Date Of Stop"], errors="coerce", format="%m/%d/%Y")
date_valid_mask = df["Date Of Stop"].notnull()
year_of_stop_mask = df["Date Of Stop"].dt.year

# Consistenza = Year <= Year of Stop
consistency_mask = df["Year"] <= year_of_stop_mask
consistency = consistency_mask.mean() * 100

# ---- Maschera combinata per righe valide ----
all_valid_mask = complete_mask & valid_mask & precise_mask & consistency_mask & date_valid_mask

# ---- Stampa delle percentuali ----
print(f"Completezza (Year): {completeness:.2f}%")
print(f"Validità (Year): {validity:.2f}%")
print(f"Precisione (Year): {precision:.2f}%")
print(f"Consistenza (Year vs Date Of Stop): {consistency:.2f}%")

# ---- Drop righe non valide ----
rows_before = len(df)
df_cleaned = df[all_valid_mask].copy()
rows_after = len(df_cleaned)

print(f"\nRighe eliminate: {rows_before - rows_after}")
print(f"Righe rimanenti: {rows_after}")

# ---- Salva i dati puliti ----
df_cleaned.to_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', index=False)
print("\nDati puliti salvati in 'Traffic_Violations_cleaned.csv'")
