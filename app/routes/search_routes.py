from flask import Blueprint, request, jsonify
import requests

from app.utils.omdb import (
    fetch_movie_by_title,
    fetch_movie_by_id,
    search_movies_by_keyword,
    fetch_random_movie,
    fetch_top_rated_movies,
)
from app.utils.omdb import random_titles

search_bp = Blueprint("search", __name__)

@search_bp.route('/search-by-title', methods=['GET'])
def search_by_title():
    title = request.args.get("title")
    year = request.args.get("year", type=int)
    plot = request.args.get("plot")

    try:
        data = fetch_movie_by_title(title, year, plot)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), 500

@search_bp.route('/search-by-id', methods=['GET'])
def search_by_id():
    movie_id = request.args.get("id")
    plot = request.args.get("plot")

    try:
        data = fetch_movie_by_id(movie_id, plot)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), 500

@search_bp.route('/search-by-keyword', methods=['GET'])
def search_by_keyword_route():
    keyword = request.args.get("keyword")
    year = request.args.get("year", type=int)
    content_type = request.args.get("content_type")
    page = request.args.get("page", type=int) or 1

    try:
        data = search_movies_by_keyword(keyword, year, content_type, page)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), 500

@search_bp.route('/search-random-movie', methods=['GET'])
def search_random_movie_route():
    plot = request.args.get("plot")

    try:
        data = fetch_random_movie(random_titles, plot)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), 500

@search_bp.route('/top-rated-movies', methods=['GET'])
def top_rated_movies_route():
    top_movies = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "Schindler's List",
    ]

    try:
        data = fetch_top_rated_movies(top_movies)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), 500


