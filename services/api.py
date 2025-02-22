import sqlite3
from constants.const import *
from constants.sql_queries import *

def get_top_players():
    result = []
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(GET_TOP_PLAYERS_QUERY)
    top_players = cursor.fetchall()
    for player in top_players:
        result.append({
            "player_id": player[7],
            "name": player[0],
            "score": player[1],
            "color": MAPPING_TEAM_COLOR[player[8]],
            "stats": [
                {"label": "currentTeam", "value": player[2]},
                {"label": "goals", "value": player[3]},
                {"label": "assists", "value": player[4]},
                {"label": "minsPlayed", "value": player[5]},
                {"label": "shotsPerGame", "value": player[6]},
            ]
            })
    cursor.execute(GET_WORST_PLAYERS_QUERY)
    worst_players = cursor.fetchall()
    for player in worst_players:
        result.append({
            "player_id": player[6],
            "name": player[0],
            "score": player[1],
            "color": MAPPING_TEAM_COLOR[player[7]],
            "stats": [
                {"label": "currentTeam", "value": player[2]},
                {"label": "minsPlayed", "value": player[3]},
                {"label": "yellowCards", "value": player[4]},
                {"label": "redCards", "value": player[5]}
            ]
        })
    cursor.close()
    conn.close()

    return result

def get_top_teams():
    result = []
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, avg_member_score, goal, possession, teamId FROM teams ORDER BY avg_member_score DESC")
    top_teams = cursor.fetchall()
    for team in top_teams:
        result.append({
            "id": team[4],
            "name": team[0],
            "score": team[1],
            "stats": [
                {"label": "goal", "value": team[2]},
                {"label": "possession", "value": team[3]}
            ]
            })
    cursor.close()
    conn.close()

    return result

def get_player_detail(player_id):
    result = []
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT date,  possitive_score, negative_score FROM histories WHERE playerId = {} ORDER BY date DESC".format(player_id))
    histories = cursor.fetchall()
    for history in histories:
        result.append({
            "date": history[0],
            "possitive_score": history[1],
            "negative_score": history[2]
        })
    cursor.close()
    conn.close()

    return result


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def get_extreme_values():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(goals + assists), MIN(goals + assists), MAX(yellowCards * 10 + redCards * 20), MIN(yellowCards * 10 + redCards * 20), MAX(passSuccess), MIN(passSuccess), MAX(150 - (yellowCards * 10 + redCards * 30)), MIN(150 - (yellowCards * 10 + redCards * 30)), MAX((height + weight) / 2), MIN((height + weight) / 2), MAX(aerialsWon), MIN(aerialsWon) FROM players")
    extremes = cursor.fetchone()
    conn.close()
    
    return tuple(safe_float(value) for value in extremes) if extremes else (150.0, 0.0, 150.0, 0.0, 150.0, 0.0, 150.0, 0.0, 150.0, 0.0, 150.0, 0.0)

def get_player_stats(player_id):
    extremes = get_extreme_values()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT goals, assists, passSuccess, yellowCards, redCards, aerialsWon, height, weight FROM players WHERE playerId = ?", (player_id,))
    player = cursor.fetchone()
    conn.close()
    
    if not player:
        return None
    
    if not player:
        return None
    
    goals, assists, pass_success, yellow_cards, red_cards, aerials_won, height, weight = map(safe_float, player)
    
    data = [
        {"subject": "Offensive", "A": goals + assists, "B": extremes[1], "fullMark": extremes[0]},
        {"subject": "Defensive", "A": yellow_cards * 10.0 + red_cards * 20.0, "B": extremes[3], "fullMark": extremes[2]},
        {"subject": "Passing", "A": pass_success, "B": extremes[5], "fullMark": extremes[4]},
        {"subject": "Discipline", "A": max(150.0 - (yellow_cards * 10.0 + red_cards * 30.0), 0.0), "B": extremes[7], "fullMark": extremes[6]},
        {"subject": "Physique", "A": (height + weight) / 2.0 if height and weight else 0.0, "B": extremes[9], "fullMark": extremes[8]},
        {"subject": "Aerials Won", "A": aerials_won, "B": extremes[11], "fullMark": extremes[10]},
    ]
    return data

def get_team_detail(team_id):
    result = []
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, avg_member_score, attack_score, defend_score, possession, discipline_score, healthy_score FROM teams WHERE teamId = {}".format(team_id))
    team = cursor.fetchone()
    result.append({
        "name": team[0],
        "stats": [
            {"label": "avg_member_score", "value": team[1] - 50, "max_value": 150},
            {"label": "attack_score", "value": team[2] / 2, "max_value": 200},
            {"label": "defend_score", "value": team[3], "max_value": 100},
            {"label": "possession", "value": team[4] * 100, "max_value": 1},
            {"label": "discipline_score", "value": 100 - team[5], "max_value": 50},
            {"label": "healthy_score", "value": team[6] * 4.5, "max_value": 22}
        ]
    })
    cursor.close()
    conn.close()

    return result