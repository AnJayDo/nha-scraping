import sqlite3
from bs4 import BeautifulSoup

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
conn = sqlite3.connect('players.db')
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