import sqlite3
from slugify import slugify
from playwright.sync_api import sync_playwright # type: ignore
from bs4 import BeautifulSoup # type: ignore
import time

def fetch_player_stats(player_id, player_name):
    """Fetch and parse match statistics for a given player."""
    url = f"https://1xbet.whoscored.com/players/{player_id}/matchstatistics/{slugify(player_name)}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')  # Wait for the page to load
        time.sleep(3)
        print("Start scraping")
        html_content = page.content()
        # Click on the 'Defensive' tab and wait for the content to load
        # page.click('a[href="#player-matches-stats-defensive"]')
        # html_content_def = page.content()
        # time.sleep(3)

        browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    stats_table = soup.find('table', {'id': 'top-player-stats-summary-grid'})
    if not stats_table:
        print(f"No statistics table found for {player_name} (ID: {player_id})")
        return None

    stats = []
    for row in stats_table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        if len(columns) < 13:
            continue  # Skip rows with insufficient data
        match = {
            'opponent': columns[0].get_text(strip=True),
            'date': columns[2].get_text(strip=True),
            'position': columns[3].get_text(strip=True),
            'minutes_played': columns[4].get_text(strip=True),
            'goals': columns[5].get_text(strip=True),
            'assists': columns[6].get_text(strip=True),
            'yellow_cards': columns[7].get_text(strip=True),
            'red_cards': columns[8].get_text(strip=True),
            'shots': columns[9].get_text(strip=True),
            'pass_success': columns[10].get_text(strip=True),
            'aerials_won': columns[11].get_text(strip=True),
            'rating': columns[12].get_text(strip=True)
        }
        stats.append(match)
    
    return stats

def store_stats(player_id, stats):
    """Store the fetched statistics into the database."""
    conn = sqlite3.connect('premier_league.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_statistics (
            player_id INTEGER,
            opponent TEXT,
            date TEXT,
            position TEXT,
            minutes_played INTEGER,
            goals INTEGER,
            assists INTEGER,
            yellow_cards INTEGER,
            red_cards INTEGER,
            shots INTEGER,
            pass_success REAL,
            aerials_won INTEGER,
            rating REAL,
            FOREIGN KEY (player_id) REFERENCES players (playerId)
        )
    ''')

    for stat in stats:
        cursor.execute('''
            INSERT INTO match_statistics (
                player_id, opponent, date, position, minutes_played, goals, assists,
                yellow_cards, red_cards, shots, pass_success, aerials_won, rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_id, stat['opponent'], stat['date'], stat['position'],
            stat['minutes_played'], stat['goals'], stat['assists'],
            stat['yellow_cards'], stat['red_cards'], stat['shots'],
            stat['pass_success'], stat['aerials_won'], stat['rating']
        ))

    conn.commit()
    conn.close()

def main():
    conn = sqlite3.connect('premier_league.db')
    cursor = conn.cursor()
    cursor.execute('SELECT playerId, name FROM players')
    players = cursor.fetchall()
    conn.close()

    for player_id, player_name in players:
        print(f"Fetching stats for {player_name} (ID: {player_id})...")
        stats = fetch_player_stats(player_id, player_name)
        if stats:
            store_stats(player_id, stats)
            print(f"Stats for {player_name} stored successfully.")
        else:
            print(f"Failed to fetch or store stats for {player_name}.")

if __name__ == '__main__':
    main()