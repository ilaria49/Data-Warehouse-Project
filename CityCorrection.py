import pandas as pd
from fuzzywuzzy import process
from tqdm import tqdm

tqdm.pandas()

# === Lista città del Maryland (pulita e in maiuscolo) ===
md_cities = [
    "ABERDEEN", "ACCOKEEK", "ADELPHI", "ANNAPOLIS", "ARBUTUS", "ARNOLD",
    "ASHTON-SANDY SPRING", "ASPEN HILL", "BALTIMORE", "BEL AIR", "BELTSVILLE",
    "BERWYN HEIGHTS", "BETHESDA", "BLADENSBURG", "BOWIE", "BRANDYWINE",
    "BROOKLYN PARK", "BURTONSVILLE", "CABIN JOHN", "CALIFORNIA", "CAPITOL HEIGHTS",
    "CATONSVILLE", "CHEVERLY", "CHEVY CHASE", "CHESTERTOWN", "CLARKSBURG",
    "CLINTON", "COCKEYSVILLE", "COLLEGE PARK", "COLUMBIA", "COTTAGE CITY",
    "CROFTON", "CUMBERLAND", "DAMASCUS", "DISTRICT HEIGHTS", "DUNDALK",
    "EASTON", "EDGEWOOD", "ELDERSBURG", "ELKRIDGE", "ELLICOTT CITY", "ESSEX",
    "FAIRMOUNT HEIGHTS", "FINKSBURG", "FOREST GLEN", "FORT MEADE", "FORT WASHINGTON",
    "FREDERICK", "GAITHERSBURG", "GAMBRILLS", "GARRISON", "GERMANTOWN",
    "GLENN DALE", "GLEN BURNIE", "GREENBELT", "HAVRE DE GRACE", "HAGERSTOWN",
    "HILLANDALE", "HUNTINGTOWN", "HYATTSVILLE", "JESSUP", "KENSINGTON",
    "LA PLATA", "LANHAM", "LANGLEY PARK", "LAUREL", "LARGO", "LEXINGTON PARK",
    "LOCHEARN", "MIDDLE RIVER", "MILLERSVILLE", "MITCHELLVILLE", "MONTGOMERY VILLAGE",
    "MOUNT AIRY", "NORTH BETHESDA", "NORTH LAUREL", "ODENTON", "OLNEY", "OXON HILL",
    "PARKVILLE", "PASADENA", "PERRY HALL", "POTOMAC", "RANDALLSTOWN", "REISTERSTOWN",
    "RIVERDALE", "ROCKVILLE", "ROSARYVILLE", "SALISBURY", "SEAT PLEASANT",
    "SEVERNA PARK", "SILVER SPRING", "SOUTH LAUREL", "SUITLAND", "TAKOMA PARK",
    "TEMPLE HILLS", "TOWSON", "UPPER MARLBORO", "WALDORF", "WESTMINSTER",
    "WHEATON", "WHITE MARSH", "WOODLAWN", "ZION"
]

# === Funzione per pulizia e fuzzy matching ===
def clean_and_match(city):
    if pd.isna(city):
        return city
    cleaned = str(city).upper().replace("MD", "").replace("RD", "").replace("PK", "")
    cleaned = cleaned.strip()
    match, score = process.extractOne(cleaned, md_cities)
    return match if score >= 85 else cleaned  # mantieni cleaned se match troppo incerto

# === Caricamento dati ===
df = pd.read_excel("infrazioni.xlsx")  # <- sostituisci col nome corretto del tuo file

# === Correzione dei nomi città ===
df['Driver City Corrected'] = df['Driver City'].progress_apply(clean_and_match)

# === Esporta il risultato in un nuovo Excel ===
df.to_excel("infrazioni_corrette.xlsx", index=False)

print("File salvato come 'infrazioni_corrette.xlsx'")
