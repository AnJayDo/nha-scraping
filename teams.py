import sqlite3
import json

# Load JSON data from file
with open("teams.json", "r", encoding="utf-8") as file:
    teams_data = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Create the `teams` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    teamId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    teamName TEXT NOT NULL,
    teamRegionName TEXT NOT NULL,
    seasonId INTEGER,
    seasonName TEXT,
    tournamentId INTEGER NOT NULL,
    isOpta BOOLEAN NOT NULL,
    tournamentRegionId INTEGER NOT NULL,
    tournamentRegionCode TEXT NOT NULL,
    tournamentRegionName TEXT NOT NULL,
    regionCode TEXT NOT NULL,
    tournamentName TEXT NOT NULL,
    rating REAL NOT NULL,
    ranking INTEGER NOT NULL,
    apps INTEGER NOT NULL,
    goal INTEGER NOT NULL,
    yellowCard INTEGER NOT NULL,
    redCard INTEGER NOT NULL,
    shotsPerGame REAL NOT NULL,
    aerialWonPerGame REAL NOT NULL,
    possession REAL NOT NULL,
    passSuccess REAL NOT NULL
)
''')

# Insert data into the `teams` table
for team in teams_data:
    cursor.execute('''
    INSERT INTO teams (
        teamId, name, teamName, teamRegionName, seasonId, seasonName, 
        tournamentId, isOpta, tournamentRegionId, tournamentRegionCode, 
        tournamentRegionName, regionCode, tournamentName, rating, ranking, 
        apps, goal, yellowCard, redCard, shotsPerGame, aerialWonPerGame, 
        possession, passSuccess
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        team["teamId"], team["name"], team["teamName"], team["teamRegionName"],
        team["seasonId"], team["seasonName"], team["tournamentId"], team["isOpta"],
        team["tournamentRegionId"], team["tournamentRegionCode"], team["tournamentRegionName"],
        team["regionCode"], team["tournamentName"], team["rating"], team["ranking"],
        team["apps"], team["goal"], team["yellowCard"], team["redCard"],
        team["shotsPerGame"], team["aerialWonPerGame"], team["possession"], team["passSuccess"]
    ))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data successfully saved to SQLite database!")