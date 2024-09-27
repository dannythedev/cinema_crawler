from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load movies from the movies.json file
def load_movies():
    with open('movies.json') as f:
        movies = json.load(f)
    return movies

# Route to serve the JSON data
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = load_movies()
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True)
