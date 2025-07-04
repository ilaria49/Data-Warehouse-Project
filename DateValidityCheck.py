import pandas as pd
from datetime import datetime

# Funzione per validare la data
def is_valid_date(value):
    try:
        print(f"Controllando data: {value}")  # Aggiungi un print per il debug
        date_obj = datetime.strptime(value, '%m/%d/%Y')
        if date_obj.month < 1 or date_obj.month > 12:
            return False
        if date_obj.day < 1 or date_obj.day > 31:
            return False
        return True
    except Exception as e:
        print(f"Errore nella data: {value} -> {e}")  # Mostra l'errore
        return False

# Funzione per validare l'orario
def is_valid_time(value):
    try:
        print(f"Controllando orario: {value}")  # Aggiungi un print per il debug
        time_obj = datetime.strptime(value, '%H:%M:%S')
        if time_obj.hour < 0 or time_obj.hour > 23:
            return False
        if time_obj.minute < 0 or time_obj.minute > 59:
            return False
        if time_obj.second < 0 or time_obj.second > 59:
            return False
        return True
    except Exception as e:
        print(f"Errore nell'orario: {value} -> {e}")  # Mostra l'errore
        return False

# Carica il dataset
df = pd.read_csv(r'C:\Users\Hp\Desktop\Traffic_Violations.csv', low_memory=False)

# Verifica la validità delle date
invalid_date_mask = ~df["Date Of Stop"].isnull() & ~df["Date Of Stop"].apply(is_valid_date)
if invalid_date_mask.sum() > 0:
    print("\n'Date Of Stop' non valide:")
    print(df.loc[invalid_date_mask, "Date Of Stop"])

# Verifica la validità degli orari
invalid_time_mask = ~df["Time Of Stop"].isnull() & ~df["Time Of Stop"].apply(is_valid_time)
if invalid_time_mask.sum() > 0:
    print("\n🚫 'Time Of Stop' non validi:")
    print(df.loc[invalid_time_mask, "Time Of Stop"])

# Droppa le righe con date o orari non validi
df = df[~invalid_date_mask & ~invalid_time_mask]

# Salva il dataset ripulito
df.to_csv(r'C:\Users\Hp\Desktop\Traffic_Violations_cleaned.csv', index=False)

print("\nDati ripuliti salvati in 'Traffic_Violations_cleaned.csv'.")
