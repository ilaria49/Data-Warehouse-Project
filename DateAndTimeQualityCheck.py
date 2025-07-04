import pandas as pd
from datetime import datetime

# Carica il dataset
df = pd.read_csv(r'C:\Users\Hp\Desktop\Traffic_Violations.csv', low_memory=False)

# Funzioni di validazione con i formati corretti
def is_valid_date(value):
    try:
        datetime.strptime(value, '%m/%d/%Y')
        return True
    except:
        return False

def is_valid_time(value):
    try:
        datetime.strptime(value, '%H:%M:%S')
        return True
    except:
        return False

# Stampa e rimozione dei non validi per "Date Of Stop"
invalid_date_mask = ~df["Date Of Stop"].isnull() & ~df["Date Of Stop"].apply(is_valid_date)
if invalid_date_mask.sum() > 0:
    print("\n🚫 Date Of Stop non valide:")
    print(df.loc[invalid_date_mask, "Date Of Stop"])
    df = df[~invalid_date_mask]

# Stampa e rimozione dei non validi per "Time Of Stop"
invalid_time_mask = ~df["Time Of Stop"].isnull() & ~df["Time Of Stop"].apply(is_valid_time)
if invalid_time_mask.sum() > 0:
    print("\n🚫 Time Of Stop non valide:")
    print(df.loc[invalid_time_mask, "Time Of Stop"])
    df = df[~invalid_time_mask]

# Funzione per statistiche
def get_stats(column, validation_func):
    total = len(df)
    non_null = df[column].notnull()
    valid = df[column][non_null].apply(validation_func)

    completeness = non_null.sum() / total * 100
    validity = valid.sum() / total * 100
    precision = (valid.sum() / non_null.sum()) * 100 if non_null.sum() else 0
    uniqueness = (df[column].duplicated().sum() / total) * 100

    return {
        "Completeness": round(completeness, 2),
        "Validity": round(validity, 2),
        "Precision": round(precision, 2),
        "Uniqueness": round(uniqueness, 2),
    }

# Calcolo statistiche aggiornate
date_stats = get_stats("Date Of Stop", is_valid_date)
time_stats = get_stats("Time Of Stop", is_valid_time)

# Consistency check: data e ora insieme
def is_consistent(row):
    try:
        if pd.isnull(row["Date Of Stop"]) or pd.isnull(row["Time Of Stop"]):
            return False
        datetime.strptime(f"{row['Date Of Stop']} {row['Time Of Stop']}", "%m/%d/%Y %H:%M:%S")
        return True
    except:
        return False

consistency = df.apply(is_consistent, axis=1).sum() / len(df) * 100

# Stampa dei risultati finali
print("\n'Date Of Stop'")
for key, value in date_stats.items():
    print(f"  {key}: {value:.2f}%")

print("\n'Time Of Stop'")
for key, value in time_stats.items():
    print(f"  {key}: {value:.2f}%")

print(f"\n🔗 Consistency (Date + Time combinabili): {consistency:.2f}%")

# (Opzionale) salva i dati ripuliti
df.to_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', index=False)
