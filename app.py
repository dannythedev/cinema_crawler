import os
from flask import Flask, jsonify
import json
import time
import datetime
# from flask_cors import CORS  # Import the CORS extension
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
            is_screenings=True
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
# CORS(app)  # Enable CORS for all routes

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
    with open('movies.json') as f:
        movies = json.load(f)
        if movies and 'Date' in movies:
            # Parse 'movies["Date"]' string to a datetime object
            movie_date = datetime.datetime.strptime(movies['Date'], "%d/%m/%Y, %H:%M")
            # Get the current datetime
            current_time = datetime.datetime.now()
            # Check if 12 hours have passed
            if (current_time - movie_date).total_seconds() >= 12 * 3600:
                data_collector = GetData()
                data_collector.start()
                return jsonify({'success': True})
        else:
            data_collector = GetData()
            data_collector.start()
            return jsonify({'success': True})
    return jsonify({'not enough time has passed.': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
