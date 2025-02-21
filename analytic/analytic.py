from constants.sql_queries import *
from constants.const import *
import sqlite3

''' Calculate the percentage of players in the game'''
def calculate_percentage_of_players_in_the_game(rule):

    print("Start calculating")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    players = []
    offset = 0

    while True:
        cursor.execute(GET_PLAYERS_PAGING_QUERY, (10, offset))
        players = cursor.fetchall()
        offset += 10
        if len(players) == 0:
            break
        else:
            for player in players:
                # cá nhân
                score = 0
                possitive_score = 0
                negative_score = 0
                # đội bóng
                attack_score = 0
                defend_score = 0

                playerId = player[0]
                teamId = player[1]
                name = player[2]
                fullName = player[3]
                currentTeam = player[4]
                shirtNumber = player[5]
                age = player[6]
                height = player[7]
                weight = player[8]
                nationality = player[9]
                positions = player[10]
                appsStr = player[11]
                minsPlayed = player[12]
                goals = player[13]
                assists = player[14]
                yellowCards = player[15]
                redCards = player[16]
                shotsPerGame = player[17]
                passSuccess = player[18]
                aerialsWon = player[19]
                motm = player[20]

                # Kiểm tra sức khỏe thực tế so với độ tuổi
                bio_age = calculate_bmr_by_age(weight, height, age)
                if bio_age <= int(age):
                    possitive_score = possitive_score + HEALTHY_SCORE

                # add motm score
                possitive_score = possitive_score + try_parse_int(motm) * MOTM_SCORE
                # get match_statictis by player_id
                cursor.execute('SELECT * FROM match_statistics WHERE player_id = {} ORDER BY date DESC'.format(playerId))
                match_statistics = cursor.fetchall()
                if len(match_statistics) > 0:
                    for match in match_statistics:
                        history_possitive_score = 0
                        history_negative_score = 0
                        # player_id = match[0]
                        # opponent = match[1]
                        date = match[2]
                        position = match[3]
                        # minutes_played = match[4]
                        goals = try_parse_int(match[5])
                        assists = try_parse_int(match[6])
                        yellow_cards = try_parse_int(match[7])
                        red_cards = try_parse_int(match[8])
                        shots = try_parse_int(match[9])
                        # pass_success = int(match[10])
                        aerials_won = try_parse_int(match[11])
                        tackles = try_parse_int(match[12])
                        interceptions = try_parse_int(match[13])
                        fouls = try_parse_int(match[14])
                        # offside_provoked = int(match[15])
                        clearances = try_parse_int(match[16])
                        challenge_lost = try_parse_int(match[17])
                        blocks = try_parse_int(match[18])
                        own_goals = try_parse_int(match[19])
                        key_passes = try_parse_int(match[20])
                        dribble_won = try_parse_int(match[21])
                        fouled = try_parse_int(match[22])
                        # offside_given = int(match[23])
                        dispossessed = try_parse_int(match[24])
                        turnovers = try_parse_int(match[25])
                        total_passes = try_parse_int(match[26])
                        pass_cross_accurate = try_parse_int(match[27])
                        pass_long_ball_accurate = try_parse_int(match[28])
                        pass_through_ball_accurate = try_parse_int(match[29])
                        
                        # add possitive score
                        history_possitive_score = history_possitive_score + rule[position]["goals"] * goals
                        history_possitive_score = history_possitive_score + rule[position]["assists"] * assists
                        history_possitive_score = history_possitive_score + rule[position]["shots"] * shots
                        history_possitive_score = history_possitive_score + rule[position]["aerials_won"] * aerials_won
                        history_possitive_score = history_possitive_score + rule[position]["tackles"] * tackles
                        history_possitive_score = history_possitive_score + rule[position]["interceptions"] * interceptions
                        history_possitive_score = history_possitive_score + rule[position]["clearances"] * clearances
                        history_possitive_score = history_possitive_score + rule[position]["blocks"] * blocks
                        history_possitive_score = history_possitive_score + rule[position]["key_passes"] * key_passes
                        history_possitive_score = history_possitive_score + rule[position]["dribble_won"] * dribble_won
                        history_possitive_score = history_possitive_score + rule[position]["fouled"] * fouled
                        history_possitive_score = history_possitive_score + rule[position]["total_passes"] * total_passes
                        history_possitive_score = history_possitive_score + rule[position]["pass_cross_accurate"] * pass_cross_accurate
                        history_possitive_score = history_possitive_score + int(rule[position]["pass_long_ball_accurate"] * pass_long_ball_accurate / 100)
                        history_possitive_score = history_possitive_score + rule[position]["pass_through_ball_accurate"] * pass_through_ball_accurate

                        # add negative score
                        history_negative_score = history_negative_score + rule[position]["own_goals"] * own_goals
                        history_negative_score = history_negative_score + rule[position]["turnovers"] * turnovers
                        history_negative_score = history_negative_score + rule[position]["dispossessed"] * dispossessed
                        history_negative_score = history_negative_score + rule[position]["fouls"] * fouls
                        history_negative_score = history_negative_score + rule[position]["challenge_lost"] * challenge_lost
                        history_negative_score = history_negative_score + rule[position]["yellow_cards"] * yellow_cards
                        history_negative_score = history_negative_score + rule[position]["red_cards"] * red_cards

                        # add score
                        score = score + history_possitive_score - history_negative_score
                        possitive_score = possitive_score + history_possitive_score
                        negative_score = negative_score + history_negative_score

                        # add attack score
                        attack_score = attack_score + rule[position]["goals"] * goals
                        attack_score = attack_score + rule[position]["assists"] * assists
                        attack_score = attack_score + rule[position]["shots"] * shots
                        attack_score = attack_score + rule[position]["aerials_won"] * aerials_won
                        attack_score = attack_score + rule[position]["key_passes"] * key_passes
                        attack_score = attack_score + rule[position]["dribble_won"] * dribble_won
                        attack_score = attack_score + rule[position]["pass_cross_accurate"] * pass_cross_accurate
                        attack_score = attack_score + rule[position]["pass_through_ball_accurate"] * pass_through_ball_accurate
                        
                        # add defend score
                        defend_score = defend_score + rule[position]["tackles"] * tackles
                        defend_score = defend_score + rule[position]["interceptions"] * interceptions
                        defend_score = defend_score + rule[position]["clearances"] * clearances
                        defend_score = defend_score + rule[position]["blocks"] * blocks


                        # insert into history table
                        cursor.execute(INSERT_HISTORY_TABLE_QUERY, (date, playerId, teamId, score, history_possitive_score, history_negative_score))
                        pass
                    # insert into players_analytics table
                cursor.execute(UPDATE_PLAYERS_SCORE_QUERY, (score, possitive_score, negative_score, attack_score, defend_score, playerId))
    print("End calculating")
    conn.commit()
    conn.close()

def calculate_team_score():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(GET_TEAMS_QUERY)
    teams = cursor.fetchall()
    for team in teams:
        team_id = team[0]
        total_score = 0
        total_player = 0
        total_healthy_score = 0
        total_attack_score = 0
        total_defend_score = 0
        total_discipline_score = 0

        cursor.execute('SELECT score, possitive_score, negative_score, age, weight, height, redCards, yellowCards, attack_score, defend_score FROM players WHERE teamId = {}'.format(team_id))
        players = cursor.fetchall()
        for player in players:
            score = player[0]
            possitive_score = try_parse_float(player[1])
            negative_score = try_parse_float(player[2])
            age = try_parse_int(player[3])
            weight = try_parse_int(player[4])
            height = try_parse_int(player[5])
            red_cards = try_parse_int(player[6])
            yellow_cards = try_parse_int(player[7])
            attack_score = try_parse_float(player[8])
            defend_score = try_parse_float(player[9])

            total_score = total_score + score
            total_player = total_player + 1

            total_discipline_score = total_discipline_score + red_cards * 3 + yellow_cards
            total_attack_score = total_attack_score + attack_score
            total_defend_score = total_defend_score + defend_score
            # Kiểm tra sức khỏe thực tế so với độ tuổi
            bio_age = calculate_bmr_by_age(weight, height, age)
            if bio_age <= int(age):
                total_healthy_score = total_healthy_score + 1

        avg_score = int(total_score / total_player)
        avg_attack_score = int(total_attack_score / total_player)
        avg_defend_score = int(total_defend_score / total_player)
        cursor.execute(UPDATE_AVG_MEMBER_SCORE_TEAM_QUERY, (avg_score, total_healthy_score, total_discipline_score, avg_attack_score, avg_defend_score, team_id))
    conn.commit()
    conn.close()
    pass

def clear_history_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM histories")
    conn.commit()
    conn.close()

def try_parse_int(value):
    try:
        return int(value)
    except:
        return 0
    
def try_parse_float(value):
    try:
        return float(value)
    except:
        return 0.0


def update_players_and_teams_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(ADD_COLUMN_SCORE_PLAYERS_QUERY)
    cursor.execute(ADD_COLUMN_POSITIVE_SCORE_PLAYERS_QUERY)
    cursor.execute(ADD_COLUMN_NEGATIVE_SCORE_PLAYERS_QUERY)
    cursor.execute(ADD_COLUMN_ATTACK_SCORE_PLAYERS_QUERY)
    cursor.execute(ADD_COLUMN_DEFEND_SCORE_PLAYERS_QUERY)
    cursor.execute(ADD_COLUMN_AVG_MEMBER_SCORE_TEAM_QUERY)
    cursor.execute(ADD_COLUMN_ATTACK_SCORE_TEAM_QUERY)
    cursor.execute(ADD_COLUMN_DEFEND_SCORE_TEAM_QUERY)
    cursor.execute(ADD_COLUMN_DISCIPLINE_SCORE_TEAM_QUERY)
    cursor.execute(ADD_COLUMN_HEALTHY_SCORE_TEAM_QUERY)
    cursor.execute(CREATE_HISTORY_TABLE_QUERY)
    conn.commit()
    conn.close()



def calculate_bmr_by_age(weight, height, age):
    bio_bmr = 10* int(weight) + 6.25* int(height) - 5*int(age) + 5
    bmr = BMR_MALE_20
    bio_age = 20
    return int(bio_age + (bmr - bio_bmr) / 5)

# print(calculate_bmr_by_age(73, 172, 36))