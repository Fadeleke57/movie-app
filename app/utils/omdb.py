import requests
import os
from dotenv import load_dotenv
from typing import Literal, Optional

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")   # Replace with your key for standalone tests
BASEURL = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&"

PlotType = Literal["short", "full"]
ContentType = Literal["movie", "series", "episode"]

def fetch_movie_by_title(title: str, year: Optional[int] = None, plot: Optional[PlotType] = None):
    """Fetch a movie by its title."""
    if not title:
        raise ValueError("Missing 'title' parameter.")

    year_param = f"&y={year}" if year else ""
    plot_param = f"&plot={plot}" if plot else ""
    api_url = f"{BASEURL}t={title}{year_param}{plot_param}"

    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def fetch_movie_by_id(movie_id: str, plot: Optional[PlotType] = None):
    """Fetch a movie by its IMDb ID."""
    if not movie_id:
        raise ValueError("Missing 'id' parameter.")

    plot_param = f"&plot={plot}" if plot else ""
    api_url = f"{BASEURL}i={movie_id}{plot_param}"

    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def search_movies_by_keyword(keyword: str, year: Optional[int] = None, content_type: Optional[ContentType] = None, page: int = 1):
    """Search movies by a keyword."""
    if not keyword:
        raise ValueError("Missing 'keyword' parameter.")
    if page < 1 or page > 100:
        raise ValueError("'page' parameter must be between 1 and 100.")

    year_param = f"&y={year}" if year else ""
    content_type_param = f"&type={content_type}" if content_type else ""
    page_param = f"&page={page}"
    api_url = f"{BASEURL}s={keyword}{year_param}{content_type_param}{page_param}"

    response = requests.get(api_url)
    response.raise_for_status()
    return response.json().get("Search", [])

def fetch_random_movie(random_titles: list, plot: Optional[PlotType] = None):
    """Fetch a random movie."""
    import random

    if not random_titles:
        raise ValueError("No random titles available.")

    title = random.choice(random_titles)
    plot_param = f"&plot={plot}" if plot else ""
    api_url = f"{BASEURL}t={title}{plot_param}"

    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def fetch_top_rated_movies(top_movies: list):
    """Fetch a predefined list of top-rated movies."""
    if not top_movies:
        raise ValueError("No top-rated movies available.")

    results = []
    for title in top_movies:
        api_url = f"{BASEURL}t={title}"
        response = requests.get(api_url)
        if response.status_code == 200:
            results.append(response.json())
    return results

random_titles = [
    "Inception",
    "Avatar",
    "The Matrix",
    "Titanic",
    "Star Wars",
    "The Godfather",
    "Pulp Fiction",
    "The Dark Knight",
    "Forrest Gump",
    "Schindler's List",
    "The Shawshank Redemption",
    "Gladiator",
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Return of the King",
    "The Lord of the Rings: The Two Towers",
    "Interstellar",
    "Fight Club",
    "Goodfellas",
    "The Silence of the Lambs",
    "Se7en",
    "Jurassic Park",
    "The Lion King",
    "Braveheart",
    "Saving Private Ryan",
    "The Prestige",
    "Whiplash",
    "Django Unchained",
    "Avengers: Endgame",
    "Black Panther",
    "The Avengers",
    "Iron Man",
    "Spider-Man: Into the Spider-Verse",
    "Frozen",
    "Coco",
    "Up",
    "WALL-E",
    "Toy Story",
    "Finding Nemo",
    "Monsters, Inc.",
    "Shrek",
    "The Truman Show",
    "The Social Network",
    "A Beautiful Mind",
    "American Beauty",
    "The Wolf of Wall Street",
    "La La Land",
    "The Grand Budapest Hotel",
    "Slumdog Millionaire",
    "The Pursuit of Happyness",
    "The Green Mile",
    "The Pianist",
    "The Great Gatsby",
    "Harry Potter and the Sorcerer's Stone",
    "Harry Potter and the Deathly Hallows: Part 2",
    "The Hunger Games",
    "Twilight",
    "The Maze Runner",
    "Divergent",
    "The Fault in Our Stars",
    "The Notebook",
    "A Star Is Born",
    "Bohemian Rhapsody",
    "Rocketman",
    "The Irishman",
    "Knives Out",
    "Parasite",
    "Jojo Rabbit",
    "The Lighthouse",
    "Once Upon a Time in Hollywood",
    "1917",
    "No Country for Old Men",
    "There Will Be Blood",
    "The Departed",
    "The Revenant",
    "Mad Max: Fury Road"
]