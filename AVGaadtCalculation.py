import pandas as pd

# === Configura i parametri principali ===
file_path = 'aadt_data.csv'  # <-- Sostituisci con il percorso del tuo file CSV
anni = [2012, 2013, 2014, 2015, 2016]
colonne_aadt = [f"AADT {anno}" for anno in anni]

# Località di interesse (puoi aggiungerne)
localita_target = ['Bethesda', 'Rockville', 'Gaithersburg', 'Germantown', 'Silver Spring', 'Wheaton']

# === Carica il file CSV ===
df = pd.read_csv(file_path)

# === Pre-elabora il nome del distretto: usa Municipality Name o Station Description ===
df['Localita'] = df['Municipality Name'].fillna('') + ' ' + df['Station Description'].fillna('')
df['Localita'] = df['Localita'].str.lower()

# === Funzione per identificare a quale località appartiene ogni riga ===
def assegna_localita(text):
    for loc in localita_target:
        if loc.lower() in text:
            return loc
    return None

df['Distretto'] = df['Localita'].apply(assegna_localita)
df_filtrato = df[df['Distretto'].notnull()]

# === Calcola la media AADT per ogni distretto nel periodo 2012–2016 ===
risultati = (
    df_filtrato.groupby('Distretto')[colonne_aadt]
    .mean()
    .round(2)
)

# === Calcola media totale sul periodo per ogni distretto ===
risultati['Indice Medio AADT 2012–2016'] = risultati.mean(axis=1).round(2)

# === Stampa i risultati ===
print("\nIndice medio AADT per distretto (2012–2016):\n")
print(risultati[['Indice Medio AADT 2012–2016']])

# === Salva su file opzionalmente ===
risultati.to_csv('indice_aadt_per_distretto.csv')
