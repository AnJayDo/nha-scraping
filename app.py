import sqlite3
from constants.const import DATABASE_NAME
import json
from analytic.analytic import calculate_percentage_of_players_in_the_game, update_players_and_teams_table, calculate_team_score, clear_history_table
from bs4 import BeautifulSoup # type: ignore


def crawl_data_from_html():
    # Sample HTML (replace this with your actual HTML content)
    html_content = """<table>...</table>"""  # Thay bằng HTML của bạn

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    # Extract headers
    headers = [th.text.strip() for th in table.find_all('th')]

    # Extract rows
    data = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = [td.text.strip() for td in row.find_all('td')]
        data.append(cols)

    # Create SQLite database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Define table schema dynamically
    columns = ', '.join([f'"{col}" TEXT' for col in headers])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS players ({columns})')

    # Insert data
    for row in data:
        placeholders = ', '.join(['?'] * len(row))
        cursor.execute(f'INSERT INTO players VALUES ({placeholders})', row)

    # Commit and close
    conn.commit()
    conn.close()

    print("Data successfully inserted into SQLite database!")


def analytic():
    clear_history_table()
    rule = json.load(open("rule.json"))
    calculate_percentage_of_players_in_the_game(rule)
    calculate_team_score()

def update_table():
    update_players_and_teams_table()


def main():
    # Step 1: Crawl data from html
    # crawl_data_from_html()

    # Step 2: Update table - only run once
    update_table()

    # Step 3: Analytic
    analytic()

    pass   


if __name__ == "__main__":
    main()
