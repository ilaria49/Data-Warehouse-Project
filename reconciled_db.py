import pandas as pd
import sqlite3

path = './xlsx/infrazioni_finali.xlsx'
db_path = 'my_database.db'

df = pd.read_excel(path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS stop;
DROP TABLE IF EXISTS violation;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS agency;
DROP TABLE IF EXISTS raw_data;

CREATE TABLE raw_data (
    -- Usa tutti i nomi e tipi possibili come TEXT per sicurezza
    "Date_Of_Stop" TEXT,
    "Time_Of_Stop" TEXT,
    Agency TEXT,
    SubAgency TEXT,
    Description TEXT,
    Location TEXT,
    Latitude REAL,
    Longitude REAL,
    Accident TEXT,
    Belts TEXT,
    Personal_Injury TEXT,
    Property_Damage TEXT,
    Fatal TEXT,
    Commercial_License TEXT,
    HAZMAT TEXT,
    Commercial_Vehicle TEXT,
    Alcohol TEXT,
    Work_Zone TEXT,
    Driver_City TEXT,
    State TEXT,
    VehicleType TEXT,
    Year INTEGER,
    Make TEXT,
    Model TEXT,
    Color TEXT,
    Violation_Type TEXT,
    Charge TEXT,
    Article TEXT,
    Contributed_To_Accident TEXT,
    Race TEXT,
    Age INTEGER,
    Gender TEXT,
    Driver_State TEXT,
    DL_State TEXT,
    Arrest_Type TEXT,
    Geolocation TEXT,
    Population INTEGER,
    Infraction_Count INTEGER,
    Speed TEXT,
    AADT INTEGER
);

CREATE TABLE agency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Agency TEXT UNIQUE,
    SubAgency TEXT
);

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Location TEXT UNIQUE,
    Latitude REAL,
    Longitude REAL,
    Geolocation TEXT,
    State TEXT,
    Population INTEGER,
    AADT INTEGER
);

CREATE TABLE driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Race TEXT,
    Gender TEXT,
    Age INTEGER,
    License_State TEXT,
    State TEXT,
    City TEXT,
    Commercial_License BOOLEAN
);

CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Color TEXT,
    Registration_Year INTEGER,
    Make TEXT,
    Model TEXT,
    Commercial_Vehicle BOOLEAN,
    Type TEXT
);

CREATE TABLE violation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Type TEXT,
    Description TEXT,
    Article TEXT,
    Charge TEXT,
    Contributed_to_Accident BOOLEAN,
    Accident BOOLEAN,
    Belts BOOLEAN,
    Alcohol BOOLEAN,
    Fatal BOOLEAN,
    Personal_Injury BOOLEAN,
    Property_Damage BOOLEAN,
    Speed BOOLEAN
);

CREATE TABLE stop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Violation_ID INTEGER,
    Vehicle_ID INTEGER,
    Driver_ID INTEGER,
    Date_of_Stop TEXT,
    Time_of_Stop TEXT,
    Workzone BOOLEAN,
    Arrest_Type TEXT,
    Agency_ID INTEGER,
    Description TEXT,
    Location_ID INTEGER,
    FOREIGN KEY (Violation_ID) REFERENCES violation(id),
    FOREIGN KEY (Vehicle_ID) REFERENCES vehicle(id),
    FOREIGN KEY (Driver_ID) REFERENCES driver(id),
    FOREIGN KEY (Agency_ID) REFERENCES agency(id),
    FOREIGN KEY (Location_ID) REFERENCES location(id)
);
""")
conn.commit()

df.to_sql('raw_data', conn, if_exists='replace', index=False)

def yes_no_to_bool(x):
    return 1 if str(x).strip().upper() == 'Y' else 0

cur.execute("""
INSERT OR IGNORE INTO agency (Agency, SubAgency)
SELECT DISTINCT Agency, SubAgency FROM raw_data WHERE Agency IS NOT NULL
""")

cur.execute("""
INSERT OR IGNORE INTO location (Location, Latitude, Longitude, Geolocation, State, Population, AADT)
SELECT DISTINCT Location, Latitude, Longitude, Geolocation, State, Population, AADT
FROM raw_data WHERE Location IS NOT NULL
""")

for _, row in df[['Race','Gender','Age','DL State','Driver State','Driver City','Commercial License']].drop_duplicates().iterrows():
    cur.execute("""
    INSERT INTO driver (Race, Gender, Age, License_State, State, City, Commercial_License)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row['Race'], row['Gender'], row['Age'],
          row['DL State'], row['Driver State'], row['Driver City'],
          yes_no_to_bool(row['Commercial License'])))
conn.commit()

for _, row in df[['Color','Year','Make','Model','Commercial Vehicle','VehicleType']].drop_duplicates().iterrows():
    cur.execute("""
    INSERT INTO vehicle (Color, Registration_Year, Make, Model, Commercial_Vehicle, Type)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (row.Color, row.Year, row.Make, row.Model,
          yes_no_to_bool(row['Commercial Vehicle']), row.VehicleType))
conn.commit()

for _, row in df[['Violation Type','Description','Article','Charge','Contributed To Accident','Accident','Belts','Alcohol','Fatal','Personal Injury','Property Damage','Speed']].drop_duplicates().iterrows():
    cur.execute("""
    INSERT INTO violation (Type, Description, Article, Charge, Contributed_to_Accident, Accident, Belts, Alcohol, Fatal, Personal_Injury, Property_Damage, Speed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row['Violation Type'], row.Description, row.Article, row.Charge,
          yes_no_to_bool(row['Contributed To Accident']), yes_no_to_bool(row.Accident), yes_no_to_bool(row.Belts),
          yes_no_to_bool(row.Alcohol), yes_no_to_bool(row.Fatal), yes_no_to_bool(row['Personal Injury']),
          yes_no_to_bool(row['Property Damage']), yes_no_to_bool(row.Speed)))
conn.commit()

for _, row in df.iterrows():
    cur.execute("SELECT id FROM violation WHERE Type=? AND Charge=? AND Article=?", (row['Violation Type'], row.Charge, row.Article))
    violation_id = cur.fetchone()
    violation_id = violation_id[0] if violation_id else None

    cur.execute("SELECT id FROM vehicle WHERE Color=? AND Registration_Year=? AND Make=? AND Model=? AND Type=?",
                (row.Color, row.Year, row.Make, row.Model, row.VehicleType))
    vehicle_id = cur.fetchone()
    vehicle_id = vehicle_id[0] if vehicle_id else None

    cur.execute("SELECT id FROM driver WHERE Race=? AND Gender=? AND Age=? AND License_State=? AND State=? AND City=?",
                (row.Race, row.Gender, row.Age, row['DL State'], row['Driver State'], row['Driver City']))
    driver_id = cur.fetchone()
    driver_id = driver_id[0] if driver_id else None

    cur.execute("SELECT id FROM agency WHERE Agency=?", (row.Agency,))
    agency_id = cur.fetchone()
    agency_id = agency_id[0] if agency_id else None

    cur.execute("SELECT id FROM location WHERE Location=?", (row.Location,))
    location_id = cur.fetchone()
    location_id = location_id[0] if location_id else None

    cur.execute("""
    INSERT INTO stop (Violation_ID, Vehicle_ID, Driver_ID, Date_of_Stop, Time_of_Stop, Workzone, Arrest_Type, Agency_ID, Description, Location_ID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (violation_id, vehicle_id, driver_id, row['Date Of Stop'], row['Time Of Stop'],
          yes_no_to_bool(row['Work Zone']), row['Arrest Type'], agency_id, row.Description, location_id))

conn.commit()
conn.close()

print("Database creato e popolato con successo!")
