import sqlite3
import time
from slugify import slugify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_player_stats(player_id, player_name):
    """Fetch and parse match statistics for a given player."""
    url = f"https://1xbet.whoscored.com/players/{player_id}/matchstatistics/{slugify(player_name)}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True to run in headless mode
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')  # Wait for the page to load
        print("Start scraping")
        html_content = page.content()
        # Click on the 'Defensive' tab and wait for the content to load
        page.click('a[href="#player-matches-stats-defensive"]')
        html_content_def = page.content()
        time.sleep(3)
        browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract Summary statistics
    summary_table = soup.find('table', {'id': 'top-player-stats-summary-grid'})
    if not summary_table:
        print(f"No summary statistics table found for {player_name} (ID: {player_id})")
        return None

    summary_stats = []
    print("Scraping Summary tab")
    for row in summary_table.find('tbody').find_all('tr'):
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
        summary_stats.append(match)

    soup_def = BeautifulSoup(html_content_def, 'html.parser')
    # Extract Defensive statistics
    defensive_table = soup_def.find('table', {'id': 'top-player-stats-summary-grid'})
    if not defensive_table:
        print(f"No defensive statistics table found for {player_name} (ID: {player_id})")
        return None

    defensive_stats = []
    print("Scraping Defensive tab")
    for row in defensive_table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        match = {
            'position': columns[3].get_text(strip=True),
            'tackles': columns[5].get_text(strip=True),
            'interceptions': columns[6].get_text(strip=True),
            'fouls': columns[7].get_text(strip=True),
            'offsides': columns[8].get_text(strip=True),
            'clearances': columns[9].get_text(strip=True),
            'dribbles': columns[10].get_text(strip=True),
            'blocks': columns[11].get_text(strip=True),
            'own_goals': columns[12].get_text(strip=True)
        }
        defensive_stats.append(match)

    # Combine Summary and Defensive statistics
    combined_stats = []
    print("Combine tabs")
    for summary, defensive in zip(summary_stats, defensive_stats):
        try:
            combined = {**summary, **defensive}
            combined_stats.append(combined)
        except Exception as e:
            print(f"An error occurred: {e}")
    for key, value in combined_stats[0].items():
        print(f"{key}: {value}")
    return combined_stats

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
            tackles INTEGER,
            interceptions INTEGER,
            fouls INTEGER,
            offsides INTEGER,
            clearances INTEGER,
            dribbles INTEGER,
            blocks INTEGER,
            own_goals INTEGER,
            rating REAL,
            FOREIGN KEY (player_id) REFERENCES players (playerId)
        )
    ''')

    for stat in stats:
        cursor.execute('''
            INSERT INTO match_statistics (
                player_id, opponent, date, position, minutes_played, goals, assists,
                yellow_cards, red_cards, shots, pass_success, aerials_won, tackles,
                interceptions, fouls, offsides, clearances, dribbles, blocks, own_goals, rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_id, stat['opponent'], stat['date'], stat['position'],
            stat['minutes_played'], stat['goals'], stat['assists'],
            stat['yellow_cards'], stat['red_cards'], stat['shots'],
            stat['pass_success'], stat['aerials_won'], stat['tackles'],
            stat['interceptions'], stat['fouls'], stat['offsides'],
            stat['clearances'], stat['dribbles'], stat['blocks'],
            stat['own_goals'], stat['rating']
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