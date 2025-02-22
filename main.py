from flask import Flask, jsonify
import secrets
import os
from services.api import get_top_players, get_top_teams, get_player_detail, get_team_detail, get_player_stats

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SECRET_KEY']=secret_key

@app.route('/top-players' , methods=['GET'])
def top_players():
    top_players = get_top_players()
    return jsonify(top_players)

@app.route('/top-teams' , methods=['GET'])
def top_teams():
    top_teams = get_top_teams()
    return jsonify(top_teams)

@app.route('/player/<player_id>' , methods=['GET'])
def player_detail(player_id):
    player_detail = get_player_stats(player_id)
    return jsonify(player_detail)

@app.route('/team/<team_id>' , methods=['GET'])
def team_detail(team_id):
    team_detail = get_team_detail(team_id)
    return jsonify(team_detail)

if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)