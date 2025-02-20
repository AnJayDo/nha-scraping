CREATE_TEAMS_TABLE_QUERY = '''
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
    )'''

INSERT_TEAMS_QUERY = '''
    INSERT INTO teams (
        teamId, name, teamName, teamRegionName, seasonId, seasonName, 
        tournamentId, isOpta, tournamentRegionId, tournamentRegionCode, 
        tournamentRegionName, regionCode, tournamentName, rating, ranking, 
        apps, goal, yellowCard, redCard, shotsPerGame, aerialWonPerGame, 
        possession, passSuccess
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

CREATE_PLAYERS_TABLE_QUERY = '''
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
    )'''

INSERT_PLAYERS_QUERY = '''
    INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

CREATE_MATCH_STATISTICS_TABLE_QUERY = '''
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
        offside_provoked INTEGER,
        clearances INTEGER,
        challenge_lost INTEGER,
        blocks INTEGER,
        own_goals INTEGER,
        key_passes INTEGER,
        dribble_won INTEGER,
        fouled INTEGER,
        offside_given INTEGER,
        dispossessed INTEGER,
        turnovers INTEGER,
        total_passes INTEGER,
        pass_cross_accurate INTEGER,
        pass_long_ball_accurate INTEGER,
        pass_through_ball_accurate INTEGER,
        rating REAL,
        FOREIGN KEY (player_id) REFERENCES players (playerId)
    )'''

INSERT_MATCH_STATISTICS_QUERY = '''
    INSERT INTO match_statistics (
        player_id, opponent, date, position, minutes_played, goals, assists,
        yellow_cards, red_cards, shots, pass_success, aerials_won, tackles,
        interceptions, fouls, offside_provoked, clearances, challenge_lost, blocks, 
        own_goals, key_passes, dribble_won, fouled, offside_given, dispossessed, 
        turnovers, total_passes, pass_cross_accurate, pass_long_ball_accurate, 
        pass_through_ball_accurate, rating
        ) 
    VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )'''
