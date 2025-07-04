import pandas as pd
from fuzzywuzzy import process
from tqdm import tqdm

tqdm.pandas()
md_cities_df = pd.read_csv("maryland_cities.csv")
md_cities = md_cities_df['City'].dropna().str.upper().tolist()
def clean_and_match(city):
    if pd.isna(city):
        return city
    cleaned = str(city).upper()
    cleaned = cleaned.strip()
    match, score = process.extractOne(cleaned, md_cities)
    return match if score >= 85 else cleaned

df = pd.read_excel("stop.xlsx")  
df['Driver City'] = df['City'].progress_apply(clean_and_match)
df.to_excel("cleaned_stop.xlsx", index=False)



