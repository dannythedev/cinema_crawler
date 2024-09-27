import os
from flask import Flask, jsonify
import json
import time
from flask_cors import CORS  # Import the CORS extension
from Archive import Archive

class GetData:
    def __init__(self):
        sources = {
            'YesPlanet': 1,
            'HotCinema': 1,
            'CinemaCity': 1,
            'LevCinema': 1,
            'Metacritic': 1,
            'RottenTomatoes': 1,
            'IMDB': 1,
            'TheMovieDB': 1,
            'Letterboxd': 0
        }
        self.archive = Archive(
            checklist=[name for name, active in sources.items() if active],
            is_screenings=False
        )

    def start(self):
        self.archive.initialize_cinemas()
        self.archive.initialize_reviewers()
        self.archive.export_json()
        print(".json exported.")

    def run_periodically(self, interval):
        while True:
            self.start()
            print("Waiting for {} seconds before the next run...".format(interval))
            time.sleep(interval)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_movies():
    with open('movies.json') as f:
        movies = json.load(f)
    return movies

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = load_movies()
    return jsonify(movies)

@app.route('/fetch', methods=['GET'])
def fetch():
    # Start fetching data in a new thread
    data_collector = GetData()
    data_collector.start()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
