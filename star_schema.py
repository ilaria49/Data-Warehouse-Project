import pandas as pd
import sqlite3

path = './xlsx/infrazioni_finali.xlsx'
db_path = 'star_schema.db'

df = pd.read_excel(path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS stop;
DROP TABLE IF EXISTS time;
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS violation;
DROP TABLE IF EXISTS arrest;
DROP TABLE IF EXISTS raw_data;

CREATE TABLE raw_data (
    -- Tutti i campi disponibili dal file originale
    "Date_Of_Stop" TEXT,
    "Time_Of_Stop" TEXT,
    Location TEXT,
    Latitude REAL,
    Longitude REAL,
    Accident TEXT,
    Belts TEXT,
    Personal_Injury TEXT,
    Property_Damage TEXT,
    Fatal TEXT,
    Commercial_License TEXT,
    Commercial_Vehicle TEXT,
    Alcohol TEXT,
    Work_Zone TEXT,
    Driver_City TEXT,
    Driver_State TEXT,
    DL_State TEXT,
    Race TEXT,
    Gender TEXT,
    Age INTEGER,
    VehicleType TEXT,
    Color TEXT,
    Make TEXT,
    Model TEXT,
    Year INTEGER,
    Violation_Type TEXT,
    Charge TEXT,
    Article TEXT,
    Arrest_Type TEXT,
    Population INTEGER,
    Speed TEXT,
    AADT INTEGER
);

CREATE TABLE time (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Year INTEGER,
    Month INTEGER,
    Quarter INTEGER,
    Date_Of_Stop TEXT,
    Time_Of_Stop TEXT
);

CREATE TABLE driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Driver_Age INTEGER,
    Driver_License_State TEXT,
    Driver_Race TEXT,
    Driver_Gender TEXT,
    Driver_State TEXT,
    Driver_City TEXT
);

CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Vehicle_Type TEXT,
    Color TEXT,
    Make TEXT,
    Model TEXT,
    Vehicle_Year INTEGER
);

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Location TEXT,
    District TEXT,
    State TEXT,
    Latitude REAL,
    Longitude REAL
);

CREATE TABLE violation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Charge TEXT,
    Article TEXT
);

CREATE TABLE arrest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Type TEXT
);

CREATE TABLE stop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    DRIVER_ID INTEGER,
    LOCATION_ID INTEGER,
    VIOLATION_ID INTEGER,
    TIME_ID INTEGER,
    VEHICLE_ID INTEGER,
    ARREST_ID INTEGER,
    Violation_count INTEGER,
    Property_damage_sum INTEGER,
    Personal_injury_sum INTEGER,
    Fatal_sum INTEGER,
    Alcohol_sum INTEGER,
    Work_zone_sum INTEGER,
    Belts_violation_sum INTEGER,
    Accident_sum INTEGER,
    Commercial_vehicle_sum INTEGER,
    Commercial_license_sum INTEGER,
    Speed_sum INTEGER,
    Population_avg REAL,
    Aadt_avg REAL,
    FOREIGN KEY (DRIVER_ID) REFERENCES driver(id),
    FOREIGN KEY (LOCATION_ID) REFERENCES location(id),
    FOREIGN KEY (VIOLATION_ID) REFERENCES violation(id),
    FOREIGN KEY (TIME_ID) REFERENCES time(id),
    FOREIGN KEY (VEHICLE_ID) REFERENCES vehicle(id),
    FOREIGN KEY (ARREST_ID) REFERENCES arrest(id)
);
""")
conn.commit()

df.to_sql('raw_data', conn, if_exists='replace', index=False)

def yes_no_to_int(val):
    return 1 if str(val).strip().upper() == 'Y' else 0


df['Year'] = pd.to_datetime(df['Date Of Stop']).dt.year
df['Month'] = pd.to_datetime(df['Date Of Stop']).dt.month
df['Quarter'] = pd.to_datetime(df['Date Of Stop']).dt.quarter
for _, row in df[['Year', 'Month', 'Quarter', 'Date Of Stop', 'Time Of Stop']].drop_duplicates().iterrows():
    cur.execute("""
        INSERT INTO time (Year, Month, Quarter, Date_Of_Stop, Time_Of_Stop)
        VALUES (?, ?, ?, ?, ?)""", tuple(row))
conn.commit()

for _, row in df[['Age','DL State','Race','Gender','Driver State','Driver City']].drop_duplicates().iterrows():
    cur.execute("""
        INSERT INTO driver (Driver_Age, Driver_License_State, Driver_Race, Driver_Gender, Driver_State, Driver_City)
        VALUES (?, ?, ?, ?, ?, ?)""", tuple(row))
conn.commit()

for _, row in df[['VehicleType','Color','Make','Model','Year']].drop_duplicates().iterrows():
    cur.execute("""
        INSERT INTO vehicle (Vehicle_Type, Color, Make, Model, Vehicle_Year)
        VALUES (?, ?, ?, ?, ?)""", tuple(row))
conn.commit()

for _, row in df[['Location','Driver State','Latitude','Longitude']].drop_duplicates().iterrows():
    cur.execute("""
        INSERT INTO location (Location, District, State, Latitude, Longitude)
        VALUES (?, NULL, ?, ?, ?)""", (row.Location, row['Driver State'], row.Latitude, row.Longitude))
conn.commit()

for _, row in df[['Charge','Article']].drop_duplicates().iterrows():
    cur.execute("""
        INSERT INTO violation (Charge, Article)
        VALUES (?, ?)""", tuple(row))
conn.commit()


for arrest_type in df['Arrest Type'].dropna().unique():
    cur.execute("INSERT INTO arrest (Type) VALUES (?)", (arrest_type,))
conn.commit()

for _, row in df.iterrows():
    cur.execute("""SELECT id FROM time WHERE Date_Of_Stop=? AND Time_Of_Stop=?""",
                (row['Date Of Stop'], row['Time Of Stop']))
    time_id = cur.fetchone()

    cur.execute("""SELECT id FROM driver WHERE Driver_Age=? AND Driver_License_State=? AND Driver_Race=? AND Driver_Gender=? AND Driver_State=? AND Driver_City=?""",
                (row['Age'], row['DL State'], row['Race'], row['Gender'], row['Driver State'], row['Driver City']))
    driver_id = cur.fetchone()

    cur.execute("""SELECT id FROM vehicle WHERE Vehicle_Type=? AND Color=? AND Make=? AND Model=? AND Vehicle_Year=?""",
                (row['VehicleType'], row['Color'], row['Make'], row['Model'], row['Year']))
    vehicle_id = cur.fetchone()

    cur.execute("""SELECT id FROM location WHERE Location=? AND State=?""", (row['Location'], row['Driver State']))
    location_id = cur.fetchone()

    cur.execute("""SELECT id FROM violation WHERE Charge=? AND Article=?""", (row['Charge'], row['Article']))
    violation_id = cur.fetchone()

    cur.execute("""SELECT id FROM arrest WHERE Type=?""", (row['Arrest Type'],))
    arrest_id = cur.fetchone()

    # Inserimento nella fact table
    cur.execute("""
        INSERT INTO stop (
            DRIVER_ID, LOCATION_ID, VIOLATION_ID, TIME_ID, VEHICLE_ID, ARREST_ID,
            Violation_count, Property_damage_sum, Personal_injury_sum, Fatal_sum,
            Alcohol_sum, Work_zone_sum, Belts_violation_sum, Accident_sum,
            Commercial_vehicle_sum, Commercial_license_sum, Speed_sum,
            Population_avg, Aadt_avg
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (driver_id[0] if driver_id else None,
         location_id[0] if location_id else None,
         violation_id[0] if violation_id else None,
         time_id[0] if time_id else None,
         vehicle_id[0] if vehicle_id else None,
         arrest_id[0] if arrest_id else None,
         1,  # Violation_count
         yes_no_to_int(row['Property Damage']),
         yes_no_to_int(row['Personal Injury']),
         yes_no_to_int(row['Fatal']),
         yes_no_to_int(row['Alcohol']),
         yes_no_to_int(row['Work Zone']),
         yes_no_to_int(row['Belts']),
         yes_no_to_int(row['Accident']),
         yes_no_to_int(row['Commercial Vehicle']),
         yes_no_to_int(row['Commercial License']),
         yes_no_to_int(row['Speed']),
         row['Population'],
         row['AADT'])
    )

conn.commit()
conn.close()

print("Database star schema creato e popolato con successo!")
