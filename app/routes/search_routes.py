from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from typing import Literal, Optional
import requests
import os

load_dotenv()

IMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASEURL = f"http://www.omdbapi.com/?apikey={IMDB_API_KEY}&"

search_bp = Blueprint("search", __name__)

SearchType = Literal["title", "id"]
PlotType = Literal["short", "full"]
ContentType = Literal["movie", "series", "episode"]

@search_bp.route('/keyword', methods=['GET'])
def search_movies_by_keyword():
    """
    Search movies by title or IMDb ID. (Exact mactches only)

    Query Parameters:
    - search_type (str): Either 'title' or 'id'.
    - value (str): The title or IMDb ID to search for.
    - year (int, optional): The year of release.
    - plot (Literal["short", "full"], optional): The length of the plot summary.

    Returns:
    A JSON object with the search results.
    """
    search_type: Optional[SearchType] = request.args.get("search_type")
    value: Optional[str] = request.args.get("value")
    year: Optional[int] = request.args.get("year", type=int)
    plot: Optional[PlotType] = request.args.get("plot")

    if not search_type or search_type not in ("title", "id"):
        return jsonify({"error": "Missing or invalid 'search_type' parameter. Must be 'title' or 'id'."}), 400

    if not value:
        return jsonify({"error": "Missing 'value' parameter."}), 400

    if plot and plot not in ("short", "full"):
        return jsonify({"error": "Invalid 'plot' parameter, must be 'short' or 'full'."}), 400

    search_key = "t" if search_type == "title" else "i"
    year_param = f"&y={year}" if year else ""
    plot_param = f"&plot={plot}" if plot else ""
    api_url = f"{BASEURL}{search_key}={value}{year_param}{plot_param}"

    response = requests.get(api_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), response.status_code
    data = response.json()

    return jsonify(data), 200

@search_bp.route('/includes', methods=['GET'])
def search_movies_by_includes():
    """
    Search content by query with optional filtering by year and content type.

    Query Parameters:
    - query (str): The search query.
    - year (int, optional): The year of release.
    - content_type (Literal["movie", "series", "episode"], optional): The type of content to search for.
    - page (int, optional): The page number to fetch.

    Returns:
    A JSON object with the search results.
    """
    search_query: str = request.args.get("query")
    release_year: Optional[int] = request.args.get("year", type=int)
    content_type: Optional[ContentType] = request.args.get("content_type")
    page: Optional[int] = request.args.get("page", type=int) or 1

    if not search_query:
        return jsonify({"error": "Missing 'query' parameter."}), 400

    if content_type and content_type not in ("movie", "series", "episode"):
        return jsonify({"error": "Invalid 'content_type' parameter. Must be 'movie', 'series', or 'episode'."}), 400
    
    if page < 1 or page > 100:
        return jsonify({"error": "'page' parameter must be between 1 and 100."}), 400

    query_param = f"&s={search_query}"
    year_param = f"&y={release_year}" if release_year else ""
    content_type_param = f"&type={content_type}" if content_type else ""
    page_param = f"&page={page}"

    api_url = f"{BASEURL}{query_param}{year_param}{content_type_param}{page_param}"

    response = requests.get(api_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OMDB API"}), response.status_code

    data = response.json()

    return jsonify(data.get("Search", [])), 200


