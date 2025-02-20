import sqlite3
import json
from contextlib import closing

from constants.const import JSON_FILE, DATABASE_NAME
from constants.sql_queries import CREATE_TEAMS_TABLE_QUERY, INSERT_TEAMS_QUERY


# Load JSON data from file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Create database and insert data
def initialize_database():
    teams_data = load_json(JSON_FILE)

    with closing(sqlite3.connect(DATABASE_NAME)) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(CREATE_TEAMS_TABLE_QUERY)
        cursor.executemany(INSERT_TEAMS_QUERY, [
            (
                team["teamId"], team["name"], team["teamName"], team["teamRegionName"],
                team.get("seasonId"), team.get("seasonName"), team["tournamentId"], team["isOpta"],
                team["tournamentRegionId"], team["tournamentRegionCode"], team["tournamentRegionName"],
                team["regionCode"], team["tournamentName"], team["rating"], team["ranking"],
                team["apps"], team["goal"], team["yellowCard"], team["redCard"],
                team["shotsPerGame"], team["aerialWonPerGame"], team["possession"], team["passSuccess"]
            ) for team in teams_data
        ])
        conn.commit()


if __name__ == "__main__":
    initialize_database()
    print("Data successfully saved to SQLite database!")
