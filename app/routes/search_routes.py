from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from typing import Literal
import requests
import os

load_dotenv()

IMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASEURL = f"http://www.omdbapi.com/?apikey={IMDB_API_KEY}&"

search_bp = Blueprint("search", __name__)

@search_bp.route('/title', methods=['GET'])
def search_movies_by_title(title : str, year : int = None, plot: Literal["short", "full"] = None):
    """
    Search movies by title.
    
    Args:
    title (str): The title of the movie
    year (int, optional): The year the movie was released. Defaults to None.
    plot (Literal["short", "full"], optional): The length of the plot. Defaults to None.
    
    Returns:
    A JSON object with the search results.
    """

@search_bp.route('/id', methods=['GET'])
def search_movies_by_id(id : str, year : int = None, plot: Literal["short", "full"] = None):
    """
    Search movies by IMDb ID.
    
    Args:
    id (str): The IMDb ID of the movie
    year (int, optional): The year the movie was released. Defaults to None.
    plot (Literal["short", "full"], optional): The length of the plot. Defaults to None.
    
    Returns:
    A JSON object with the search results.
    """



