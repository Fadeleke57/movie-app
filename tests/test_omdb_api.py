import pytest
from unittest.mock import patch
from app.utils.omdb import (
    fetch_movie_by_title,
    fetch_movie_by_id,
    search_movies_by_keyword,
    fetch_random_movie,
    fetch_top_rated_movies,
)

@pytest.fixture
def mock_requests_get():
    """Fixture to mock the requests.get method."""
    with patch("app.utils.omdb.requests.get") as mock_get:
        yield mock_get

def test_fetch_movie_by_title(mock_requests_get):
    """
    Test the fetch_movie_by_title function.

    Test that the function returns the movie title, when given a valid title.
    """
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"Title": "Inception"}
    
    result = fetch_movie_by_title("Inception")
    assert result["Title"] == "Inception"

def test_fetch_movie_by_title_missing_title():
    """
    Test that the fetch_movie_by_title function raises a ValueError
    when given an empty 'title' parameter.
    """
    with pytest.raises(ValueError, match="Missing 'title' parameter."):
        fetch_movie_by_title("")

def test_fetch_movie_by_id(mock_requests_get):
    """
    Test the fetch_movie_by_id function.

    Test that the function returns the movie title, when given a valid IMDb ID.
    """
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"Title": "Inception"}
    
    result = fetch_movie_by_id("tt1375666")
    assert result["Title"] == "Inception"

def test_fetch_movie_by_id_missing_id():
    """
    Test that the fetch_movie_by_id function raises a ValueError
    when given an empty 'id' parameter.
    """
    with pytest.raises(ValueError, match="Missing 'id' parameter."):
        fetch_movie_by_id("")

def test_search_movies_by_keyword(mock_requests_get):
    """
    Test the search_movies_by_keyword function.

    Test that the function returns the movie title, when given a valid keyword.
    """
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"Search": [{"Title": "Inception"}]}
    
    result = search_movies_by_keyword("Inception")
    assert result[0]["Title"] == "Inception"

def test_search_movies_by_keyword_invalid_page():
    """
    Test that the search_movies_by_keyword function raises a ValueError
    when given an invalid 'page' parameter.
    """
    with pytest.raises(ValueError, match="'page' parameter must be between 1 and 100."):
        search_movies_by_keyword("Inception", page=101)

def test_fetch_random_movie(mock_requests_get):
    """
    Test the fetch_random_movie function.

    Test that the function returns the movie title when given a list of valid titles.
    """
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"Title": "Inception"}
    
    result = fetch_random_movie(["Inception", "Avatar"])
    assert result["Title"] == "Inception"

def test_fetch_random_movie_empty_titles():
    """
    Test that the fetch_random_movie function raises a ValueError
    when given an empty list of titles.
    """
    with pytest.raises(ValueError, match="No random titles available."):
        fetch_random_movie([])

def test_fetch_top_rated_movies(mock_requests_get):
    """
    Test the fetch_top_rated_movies function.

    Test that the function returns the top rated movies when given a list of valid titles.
    """
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"Title": "The Godfather"}
    
    result = fetch_top_rated_movies(["The Godfather"])
    assert result[0]["Title"] == "The Godfather"

def test_fetch_top_rated_movies_empty_list():
    """
    Test that the fetch_top_rated_movies function raises a ValueError
    when given an empty list of top rated movies.
    """
    with pytest.raises(ValueError, match="No top-rated movies available."):
        fetch_top_rated_movies([])