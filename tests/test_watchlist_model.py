import pytest
from app import create_app
from app.utils.db import db
from unittest.mock import Mock
from app.utils.watchlist_utils import add_movie_to_watchlist

@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    return app

@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()

@pytest.fixture
def init_db(app):
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

#Mock user query
@pytest.fixture
def mock_user_query(mocker, app):
    with app.app_context():
        mock_user_query = Mock()
        mock_user = Mock(id=1, username="test_user")
        mock_user_query.filter_by.return_value.first.return_value = mock_user
        mocker.patch("app.models.user.User.query", mock_user_query)
        return mock_user_query

#Mock watchlist query
@pytest.fixture
def mock_watchlist_query(mocker, app):
    with app.app_context():
        mock_watchlist_query = Mock()
        mock_watchlist_query.filter_by.return_value.first.return_value = None
        mocker.patch("app.models.watchlist.Watchlist.query", mock_watchlist_query)
        return mock_watchlist_query

#Mock movie by id
@pytest.fixture
def mock_fetch_movie_by_id(mocker, app):
    with app.app_context():
        mock_fetch_movie_by_id = Mock()
        mock_fetch_movie_by_id.return_value = {
            "title": "Elf",
            "imdb_id": "tt0319343",
            "year": "2021",
            "rated": "PG",
            "runtime": "97 min",
            "plot": "Raised as an oversized elf, Buddy travels from the North Pole to New York City to meet his biological father, Walter Hobbs, who doesn't know he exists and is in desperate need of some Christmas spirit.",
            "genre": "Adventure, Comedy, Family",
            "imdb_rating": "7.1",
            "type": "movie"
        }
        mocker.patch("app.utils.watchlist_utils.fetch_movie_by_id", mock_fetch_movie_by_id)
        return mock_fetch_movie_by_id

#Mock database
@pytest.fixture
def mock_db_session(mocker, app):
    with app.app_context():
        mock_db_session = Mock()
        mocker.patch("app.utils.db.db.session", mock_db_session)
        return mock_db_session

#Test if adding was successful
def test_add_movie_to_watchlist_successful(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_watchlist_query.filter_by.return_value.first.return_value = None
    mock_user = mock_user_query.filter_by.return_value.first.return_value
    username = mock_user.username     
    movie_data = mock_fetch_movie_by_id()
    imdb_id = movie_data["imdb_id"]

    assert username == "test_user"
    assert imdb_id == "tt0319343"

    add_movie_to_watchlist(username, imdb_id)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    added_watchlist_item = mock_db_session.add.call_args[0][0]
    assert added_watchlist_item.user_id == mock_user.id 
    assert added_watchlist_item.imdb_id == imdb_id 

#Test if adding was usuccessful because user not found
def test_add_movie_to_watchlist_user_not_found(mock_user_query):
    mock_user_query.filter_by.return_value.first.return_value = None
    with pytest.raises(ValueError, match="User not found"):
        add_movie_to_watchlist("non_existent_user", "tt1234567")

#Test if adding was usuccessful because movie not found
def test_add_movie_to_watchlist_movie_not_found(mock_fetch_movie_by_id):
    mock_fetch_movie_by_id.return_value = None  
    with pytest.raises(ValueError, match="Movie not found"):
        add_movie_to_watchlist("test_user", "tt1234567")

#Test add duplicates
def test_add_movie_already_in_watchlist(mock_user_query, mock_fetch_movie_by_id, mock_watchlist_query):
    mock_user = mock_user_query.filter_by.return_value.first.return_value
    username = mock_user.username     
    movie_data = mock_fetch_movie_by_id()
    imdb_id = movie_data["imdb_id"]

    mock_watchlist_query.filter_by.return_value.first.return_value = Mock(imdb_id=imdb_id)  # Movie exists

    with pytest.raises(ValueError, match="Movie 'Elf' is already in test_user's watchlist."):
        add_movie_to_watchlist(username, imdb_id)