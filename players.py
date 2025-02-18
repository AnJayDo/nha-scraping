import sqlite3
from bs4 import BeautifulSoup
import time
from slugify import slugify
from playwright.sync_api import sync_playwright, Playwright
import os

# Function to convert team name to a slug format
def team_name_to_slug(name):
    return slugify(text=name, allow_unicode=True)

# Helper function to convert country code to full country name
def get_country_name(country_code):
    # Add a mapping of country codes to full names
    country_mapping = {
        "eg": "Egypt",
        "gb-eng": "England",
        "co": "Colombia",
        "nl": "Netherlands",
        "ar": "Argentina",
        "fr": "France",
        "hu": "Hungary",
        "br": "Brazil",
        "pt": "Portugal",
        "gb-sct": "Scotland",
        "ie": "Ireland",
        "gr": "Greece",
        "uy": "Uruguay",
        "cz": "Czech Republic",
        "gb-nir": "Northern Ireland",
        "it": "Italy",
        "jp": "Japan",
    }
    return country_mapping.get(country_code.lower(), "Unknown")

# Function to scrape player details from a team page
def scrape_players(team_id, team_name):
    url = f"https://1xbet.whoscored.com/teams/{team_id}/show/england-{team_name_to_slug(team_name)}"
    print(f"Scraping players from: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        try:
            page.goto(url)  # Navigate to the URL
            page.wait_for_load_state('networkidle')  # Wait for the page to load
            time.sleep(3)

            # Wait for the element with the class 'team-squad-stats-summary'
            # print("Waiting for team-squad-stats-summary to be visible")
            # page.wait_for_selector(".team-squad-stats-summary", state="attached")
            print("Tag team-squad-stats-summary is attached")

            # Get the page HTML after JavaScript rendering
            page_content = page.content()

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(page_content, "html.parser")

            # Define the directory and filename
            directory = "teams"
            filename = f"{team_name_to_slug(team_name)}.html"
            file_path = os.path.join(directory, filename)

            # Create the 'teams' directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)

            # Write the parsed HTML to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(soup))
                
            # Find all player containers
            players = []
            print("Start getting players")

            for player in soup.find_all("tr", class_=lambda x: x and (" " in x or "alt" in x)):
                try:
                    # Extract player ID from the href attribute
                    player_link = player.find("a", class_="player-link")
                    href = player_link["href"]
                    player_id = int(href.split("/")[2])  # Extract ID from href

                    # Extract name
                    name = player_link.find("span", class_="iconize").text.strip()
                    print(f"{name} was caught.")

                    # Extract full name (if available, otherwise use name)
                    full_name = name  # Default to name if full name is not available

                    # Extract shirt number (This might need better parsing)
                    shirt_number = player.find("span", class_="player-meta-data").text.strip().split(",")[0]
                    print(f"{shirt_number} was shirt number.")

                    # Extract age (Handle more robustly)
                    age_tag = player.find("span", class_="player-meta-data")
                    age = None
                    if age_tag:
                        # The age is the first part before the comma
                        age = int(age_tag.text.strip().split(",")[0])
                    print(f"{age} was age.")

                    # Extract height and weight
                    height = player.find_all("td")[2].text.strip() if len(player.find_all("td")) > 2 else None
                    weight = player.find_all("td")[3].text.strip() if len(player.find_all("td")) > 3 else None

                    # Extract other stats
                    apps_str = player.find_all("td")[4].get_text(strip=True)
                    mins_played = player.find_all("td")[5].get_text(strip=True)
                    goals = player.find_all("td")[6].get_text(strip=True)
                    assists = player.find_all("td")[7].get_text(strip=True)
                    yellow_cards = player.find_all("td")[8].get_text(strip=True)
                    red_cards = player.find_all("td")[9].get_text(strip=True)
                    shots_per_game = player.find_all("td")[10].get_text(strip=True)
                    pass_success = player.find_all("td")[11].get_text(strip=True)
                    aerials_won = player.find_all("td")[12].get_text(strip=True)
                    motm = player.find_all("td")[13].get_text(strip=True)
                    rating = player.find_all("td")[14].get_text(strip=True)

                    # Extract nationality (country name) from the flag class
                    flag_class = player.find("span", class_="ui-icon country")
                    nationality = None
                    if flag_class:
                        flag_class = flag_class.get("class", [])
                        if flag_class:
                            country_code = flag_class[-1].split("-")[-1]  # Extract country code
                            nationality = get_country_name(country_code)  # Convert code to full name

                    # Extract positions (this is inside player-meta-data, can be multiple)
                    positions = None
                    player_meta_data_spans = player.find_all("span", class_="player-meta-data")
                    if len(player_meta_data_spans) > 1:
                        positions = player_meta_data_spans[1].text.strip()

                    # Append player data to the list
                    players.append((player_id, team_id, name, full_name, team_name, shirt_number, age, height, weight, nationality, positions, 
                                    apps_str, mins_played, goals, assists, yellow_cards, red_cards, shots_per_game, pass_success, aerials_won,
                                    motm, rating))
                except Exception as e:
                    print(f"Error parsing player: {e}")
                    continue
            
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
            players = []
        finally:
            browser.close()  # Make sure to close the browser

    return players

# Connect to SQLite database
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Create `players` table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    playerId INTEGER PRIMARY KEY,
    teamId INTEGER NOT NULL,
    name TEXT NULL,
    fullName TEXT NULL,
    currentTeam TEXT NULL,
    shirtNumber TEXT NULL,
    age TEXT NULL,
    height TEXT NULL,
    weight TEXT NULL,
    nationality TEXT NULL,
    positions TEXT NULL,
    appsStr TEXT NULL,
    minsPlayed TEXT NULL, 
    goals TEXT NULL, 
    assists TEXT NULL,
    yellowCards TEXT NULL,
    redCards TEXT NULL, 
    shotsPerGame TEXT NULL, 
    passSuccess TEXT NULL, 
    aerialsWon TEXT NULL,
    motm TEXT NULL, 
    rating TEXT NULL,
    FOREIGN KEY (teamId) REFERENCES teams(teamId)
)
''')

# Fetch teams from SQLite
cursor.execute("SELECT teamId, teamName FROM teams")
teams = cursor.fetchall()

for team_id, team_name in teams:
    print(f"Scraping players for team: {team_name} (ID: {team_id})")
    players = scrape_players(team_id, team_name)
    
    if not players:
        print(f"No players found for {team_name}. Skipping.")
        continue
    
    for player in players:
        try:
            cursor.execute('''
                INSERT INTO players (
                    playerId, 
                    teamId, 
                    name, 
                    fullName, 
                    currentTeam, 
                    shirtNumber, 
                    age, 
                    height, 
                    weight, 
                    nationality, 
                    positions, 
                    appsStr, 
                    minsPlayed, 
                    goals, 
                    assists, 
                    yellowCards, 
                    redCards, 
                    shotsPerGame, 
                    passSuccess, 
                    aerialsWon, 
                    motm, 
                    rating
                )
                VALUES (
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?)
            ''', player)
        except sqlite3.Error as e:
            print(f"❌ Error inserting player data into database: {e}")
    
    conn.commit()
    time.sleep(2)  # Delay to avoid rate limiting

# Close connection
conn.close()
print("✅ Player data successfully saved to SQLite!")