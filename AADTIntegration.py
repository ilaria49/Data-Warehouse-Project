import pandas as pd

# === Percorso del file CSV ===
file_path = 'annual.xlsx'  # <-- Cambia con il tuo percorso reale

# === Anni da considerare ===
colonne_aadt = ['AADT 2012', 'AADT 2013', 'AADT 2014', 'AADT 2015', 'AADT 2016']

# === Località da analizzare ===
localita_target = ['BALTIMORE', 'Silver Spring', 'Germantown', 'Gaithersburg', 'Rockville', 'Bethesda', "MONTGOMERY"]

# === Caricamento del file ===
df = pd.read_excel(file_path)
df['LocalitaTesto'] = (
    df['Municipality Name'].fillna('') + ' ' +
    df['Station Description'].fillna('')
).str.lower()

# === Funzione per assegnare il distretto ===
def assegna_distretto(text):
    for nome in localita_target:
        if nome.lower() in text:
            return nome
    return None

df['Distretto'] = df['LocalitaTesto'].apply(assegna_distretto)

# === Filtra solo righe con distretti noti ===
df_filtrato = df[df['Distretto'].notnull()].copy()

# === Converte colonne AADT in numerico ===
for col in colonne_aadt:
    df_filtrato[col] = pd.to_numeric(df_filtrato[col], errors='coerce')

# === Calcola l'indice medio per ogni distretto e anno ===
risultati = df_filtrato.groupby('Distretto')[colonne_aadt].mean().round(2)

# === Visualizza risultati ===
print("\nIndice medio AADT per distretto e anno (2014–2016):\n")
print(risultati)

# === Salva su CSV se vuoi ===
risultati.to_csv('indice_medio_per_distretto_per_anno.csv')