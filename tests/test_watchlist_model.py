import pytest
from app import create_app
from app.utils.db import db
from unittest.mock import Mock
from app.utils.watchlist_utils import (
    add_movie_to_watchlist,
    delete_movie_from_watchlist,
    update_movie_from_watchlist,
    get_user_watchlist
)

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
            "Title": "Elf",
            "imdbID": "tt0319343",
            "Year": "2021",
            "Rated": "PG",
            "Runtime": "97 min",
            "Plot": "Raised as an oversized elf, Buddy travels from the North Pole to New York City to meet his biological father, Walter Hobbs, who doesn't know he exists and is in desperate need of some Christmas spirit.",
            "Genre": "Adventure, Comedy, Family",
            "imdbRating": "7.1",
            "Type": "movie"
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
    mock_fetch_movie_by_id.return_value = {
            "Title": "Elf",
            "imdbID": "tt0319343",
            "Year": "2021",
            "Rated": "PG",
            "Runtime": "97 min",
            "Plot": "Raised as an oversized elf, Buddy travels from the North Pole to New York City to meet his biological father, Walter Hobbs, who doesn't know he exists and is in desperate need of some Christmas spirit.",
            "Genre": "Adventure, Comedy, Family",
            "imdbRating": "7.1",
            "Type": "movie"
        }
    movie_data = mock_fetch_movie_by_id.return_value
    imdb_id = movie_data["imdbID"]

    assert username == "test_user"
    assert imdb_id == "tt0319343"

    add_movie_to_watchlist(username, imdb_id)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    added_watchlist_item = mock_db_session.add.call_args[0][0]
    assert added_watchlist_item.user_id == mock_user.id 
    assert added_watchlist_item.imdb_id == imdb_id 

#Test if adding was unsuccessful because user not found
def test_add_movie_to_watchlist_user_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user_query.filter_by.return_value.first.return_value = None
    with pytest.raises(ValueError, match="User not found"):
        add_movie_to_watchlist("non_existent_user", "tt1234567")

#Test if adding was unsuccessful because movie not found
def test_add_movie_to_watchlist_movie_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_fetch_movie_by_id.return_value = None

    mock_user_query.filter_by.return_value.first.return_value = Mock(id=1, username="test_user")
    with pytest.raises(ValueError, match="Movie not found"):
            add_movie_to_watchlist("test_user", "tt1234567")

#Test add duplicates
def test_add_movie_already_in_watchlist(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = mock_user_query.filter_by.return_value.first.return_value
    username = mock_user.username     
    mock_fetch_movie_by_id.return_value = {
            "Title": "Elf",
            "imdbID": "tt0319343",
            "Year": "2021",
            "Rated": "PG",
            "Runtime": "97 min",
            "Plot": "Raised as an oversized elf, Buddy travels from the North Pole to New York City to meet his biological father, Walter Hobbs, who doesn't know he exists and is in desperate need of some Christmas spirit.",
            "Genre": "Adventure, Comedy, Family",
            "imdbRating": "7.1",
            "Type": "movie"
        }
    movie_data = mock_fetch_movie_by_id.return_value
    imdb_id = movie_data["imdbID"]

    mock_watchlist_query.filter_by.return_value.first.return_value = Mock(imdb_id=imdb_id)  # Movie exists

    with pytest.raises(ValueError, match="Movie 'Elf' is already in test_user's watchlist."):
        add_movie_to_watchlist(username, imdb_id)

#Test if deleting was successful
def test_delete_movie_from_watchlist_successful(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    movie_data = { "title": "Elf", "imdb_id": "tt0319343"}
    mock_fetch_movie_by_id.return_value = movie_data
    imdb_id = movie_data["imdb_id"]

    mock_watchlist_entry = Mock(user_id=mock_user.id, imdb_id=imdb_id)
    mock_watchlist_query.filter_by.return_value.first.return_value = mock_watchlist_entry

    assert username == "test_user"
    assert imdb_id == "tt0319343"

    delete_movie_from_watchlist(username, imdb_id)
    
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
    deleted_watchlist_item = mock_db_session.delete.call_args[0][0]
    assert deleted_watchlist_item.user_id == mock_user.id 
    assert deleted_watchlist_item.imdb_id == imdb_id 

#Test if deleting was unsuccessful because user not found
def test_delete_movie_from_watchlist_user_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user_query.filter_by.return_value.first.return_value = None
    with pytest.raises(ValueError, match="User not found"):
        delete_movie_from_watchlist("non_existent_user", "tt1234567")

#Test if deleting was unsuccessful because watchlist entry not found
def test_delete_movie_from_watchlist_watchlist_entry_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    movie_data = { "title": "Elf", "imdb_id": "tt0319343"}
    mock_fetch_movie_by_id.return_value = movie_data
    imdb_id = movie_data["imdb_id"]
    
    mock_watchlist_query.filter_by.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Watchlist entry not found"):
        delete_movie_from_watchlist(username, imdb_id)

#Test if updating was successful
def test_update_movie_from_watchlist_successful(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    mock_fetch_movie_by_id.return_value = {
            "Title": "Elf",
            "imdbID": "tt0319343",
            "Year": "2021",
            "Rated": "PG",
            "Runtime": "97 min",
            "Plot": "Raised as an oversized elf, Buddy travels from the North Pole to New York City to meet his biological father, Walter Hobbs, who doesn't know he exists and is in desperate need of some Christmas spirit.",
            "Genre": "Adventure, Comedy, Family",
            "imdbRating": "7.1",
            "Type": "movie"
        }
    movie_data = mock_fetch_movie_by_id.return_value
    imdb_id = movie_data["imdbID"]

    mock_watchlist_entry = Mock(user_id=mock_user.id, imdb_id=imdb_id, watching_state="To Watch")
    mock_watchlist_query.filter_by.return_value.first.return_value = mock_watchlist_entry

    assert username == "test_user"
    assert imdb_id == "tt0319343"
    new_state = "Watch Next"

    update_movie_from_watchlist(username, imdb_id, new_state)
    
    mock_db_session.commit.assert_called_once()
    assert mock_watchlist_entry.watching_state == new_state
    assert mock_watchlist_entry.imdb_id == imdb_id
    assert mock_watchlist_entry.user_id == mock_user.id
   
#Test if updating was unsuccessful because user not found
def test_update_movie_from_watchlist_user_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user_query.filter_by.return_value.first.return_value = None
    with pytest.raises(ValueError, match="User not found"):
        update_movie_from_watchlist("non_existent_user", "tt1234567", "Watch Next")

#Test if updating was unsuccessful because watchlist entry not found
def test_update_movie_from_watchlist_watchlist_entry_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    movie_data = { "title": "Elf", "imdb_id": "tt0319343"}
    mock_fetch_movie_by_id.return_value = movie_data
    imdb_id = movie_data["imdb_id"]
    
    mock_watchlist_query.filter_by.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Watchlist entry not found"):
        update_movie_from_watchlist(username, imdb_id, "Watch Next")

#Test if updating was unsuccessful because invalid watching state inputted not found
def test_update_movie_from_watchlist_invalid_watching_state(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    movie_data = { "title": "Elf", "imdb_id": "tt0319343"}
    mock_fetch_movie_by_id.return_value = movie_data
    imdb_id = movie_data["imdb_id"]

    mock_watchlist_entry = Mock(user_id=mock_user.id, imdb_id=imdb_id, watching_state="To Watch")
    mock_watchlist_query.filter_by.return_value.first.return_value = mock_watchlist_entry
    new_state = "None"

    with pytest.raises(ValueError, match="New state must be 'To Watch' or 'Watched' or 'Watch Next'"):
        update_movie_from_watchlist(username, imdb_id, new_state)

#Test if getting user watchlist was successful
def test_get_watchlist_successful(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user = Mock(id=1, username="test_user")
    mock_user_query.filter_by.return_value.first.return_value = mock_user
    username = mock_user.username

    movie_data = {   
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
    
    mock_fetch_movie_by_id.return_value = movie_data
    imdb_id = movie_data["imdb_id"]
    title = movie_data["title"]
    year = movie_data["year"]
    rated = movie_data["rated"]
    runtime = movie_data["runtime"]
    plot = movie_data["plot"]
    genre = movie_data["genre"]
    imdb_rating = movie_data["imdb_rating"]
    type = movie_data["type"]

    mock_watchlist_entry1 = Mock(user_id=mock_user.id, title=title, year=year, rated=rated, runtime=runtime, plot=plot, genre=genre, imdb_rating=imdb_rating, type=type, imdb_id=imdb_id, watching_state="To Watch")
    mock_watchlist_entry2 = Mock(user_id=2, title=title, year=year, rated=rated, runtime=runtime, plot=plot, genre=genre, imdb_rating=imdb_rating, type=type, imdb_id=imdb_id, watching_state="To Watch")

    filtered_entries = []
    for entry in [mock_watchlist_entry1, mock_watchlist_entry2]:
        if entry.user_id == mock_user.id:
            filtered_entries.append(entry)

    mock_watchlist_query.filter_by.return_value.all = Mock(return_value=filtered_entries)

    assert username == "test_user"
    assert imdb_id == "tt0319343"
    user_watchlist = get_user_watchlist(username)

    expected_user_watchlist = [{
        'imdbID': mock_watchlist_entry1.imdb_id,
        'Title': movie_data['title'],
        'Year': movie_data["year"],
        'Rated': movie_data["rated"],  
        'Runtime': movie_data["runtime"],  
        'Plot': movie_data["plot"], 
        'Genre': movie_data["genre"],  
        'imdbRating': movie_data["imdb_rating"], 
        'Type': movie_data["type"],  
        'Watching State': mock_watchlist_entry1.watching_state
    }]

    assert user_watchlist == expected_user_watchlist

#Test if getting watchlist was unsuccessful because user not found
def test_get_watchlist_user_not_found(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_user_query.filter_by.return_value.first.return_value = None
    with pytest.raises(ValueError, match="User not found"):
        get_user_watchlist("non_existent_user")

#Test if getting watchlist was unsuccessful because watchlist has no movies
def test_get_watchlist_no_movies(mock_db_session, mock_user_query, mock_watchlist_query, mock_fetch_movie_by_id):
    mock_watchlist_query.filter_by.return_value.all = Mock(return_value=[])
    with pytest.raises(ValueError, match="No movies found in watchlist for test_user"):
        get_user_watchlist("test_user")


