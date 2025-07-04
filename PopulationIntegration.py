import pandas as pd

# Carica il file dei fermi (Excel)
stops_df = pd.read_excel("stops.xlsx")  # Colonne: Date Of Stop, Race

# Carica il file della popolazione (CSV), con gli anni come indice
population_df = pd.read_csv("population.csv", index_col=0)

# Normalizza i nomi delle colonne della popolazione (es. NATIVE AM → NATIVE AMERICAN)
population_df.columns = [col.strip().upper() for col in population_df.columns]

# Parsing della data nel formato MM/DD/YYYY
stops_df['Year'] = pd.to_datetime(stops_df['Date Of Stop'], format='%m/%d/%Y').dt.year

# Funzione per cercare la popolazione
def get_population(row):
    year = row['Year']
    race = row['Race'].strip().upper()
    try:
        return population_df.at[year, race]
    except KeyError:
        return None  # oppure np.nan

# Applica la funzione
stops_df['Population'] = stops_df.apply(get_population, axis=1)

# Salva il risultato
stops_df.to_excel("stops_with_population.xlsx", index=False)
