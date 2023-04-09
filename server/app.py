import csv
from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app, supports_credentials=True)

def read_csv_file():
    games = []
    with open('server/steam.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games.append(row)
    return games

library_games = []
all_games = read_csv_file()

@app.route('/games', methods=['GET'])
def get_games():
    return jsonify(library_games)   

@app.route('/games', methods=['POST'])
def add_game():
    game = request.json
    library_games.append(game)
    return jsonify(game)

@app.route('/games/<appid>', methods=['PUT'])
def update_game(appid):
    game = next((g for g in library_games if g['appid'] == appid), None)
    if game:
        updates = request.json
        for key, value in updates.items():
            game[key] = value
        return jsonify(game)
    else:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/games/<appid>', methods=['DELETE'])
def delete_game(appid):
    game = next((g for g in library_games if g['appid'] == appid), None)
    if game:
        library_games.remove(game)
        return jsonify({'result': 'Game removed'})
    else:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/search_games', methods=['POST'])
def search_games():
    search_query = request.json['searchQuery']
    filter_type = request.json['filterType']
    search_results = [
        game for game in all_games
        if search_query.lower() in game[filter_type].lower()
    ]
    return jsonify(search_results)


if __name__ == '__main__':
    app.run(debug=True)
