from app.models.user import User
from app.models.watchlist import Watchlist
from app.utils.omdb import fetch_movie_by_id
from app.utils.db import db
from app.utils.logger import logger


def add_movie_to_watchlist(username, imdb_id):
    """
    Adds a movie to user's watchlist.

    Arguments:
        username (str): The username of user.
        imdb_id (str): The IMDb of the movie.

    Raises:
        ValueError: If user is not found.
        ValueError: If movie is not found.
        ValueError: If user and movie already exists.
    """

    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError("User not found")
    
    movie = fetch_movie_by_id(imdb_id)
    if not movie:
        raise ValueError("Movie not found")

    existing_entry = Watchlist.query.filter_by(user_id=user.id, imdb_id=imdb_id).first()
    if existing_entry:
        raise ValueError(f"Movie '{movie.get('Title')}' is already in {username}'s watchlist.")

    
    watchlist = Watchlist(
        user_id = user.id,
        title = movie.get('Title'),
        imdb_id=movie.get('imdbID'),
        year=movie.get('Year'),
        rated=movie.get('Rated'),
        runtime=movie.get('Runtime'),
        plot=movie.get('Plot'),
        genre=movie.get('Genre'),
        imdb_rating=movie.get('imdbRating'),
        type=movie.get('Type'),
        watching_state="To Watch" 
    )

    db.session.add(watchlist)
    db.session.commit()

    logger.info(f"Added movie '{movie.get('Title')}' to {username}'s watchlist successfully.")

def delete_movie_from_watchlist(username, imdb_id):
    """
    Deletes a movie from user's watchlist.

    Arguments:
        username (str): The username of user.
        imdb_id (str): The IMDb of the movie.

    Raises:
        ValueError: If user is not found.
        ValueError: If watchlist entry is not found.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError("User not found")

    watchlist_entry = Watchlist.query.filter_by(user_id=user.id, imdb_id=imdb_id).first()
    if not watchlist_entry:
        raise ValueError("Watchlist entry not found")

    db.session.delete(watchlist_entry)
    db.session.commit()

    logger.info(f"Deleted movie '{watchlist_entry.title}' from {username}'s watchlist successfully.")

def update_movie_from_watchlist(username, imdb_id, new_state):
    """
    Updates a movie and its watching state from user's watchlist.
    Deletes movie if state is updated to watched.

    Arguments:
        username (str): The username of user.
        imdb_id (str): The IMDb of the movie.
        new_state (str): The new watching state of the movie.

    Raises:
        ValueError: If user is not found.
        ValueError: If watchlist entry is not found.
        ValueError: If watch state is not 'To Watch' or 'Watched' or 'Watch Next'.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError("User not found")

    watchlist_entry = Watchlist.query.filter_by(user_id=user.id, imdb_id=imdb_id).first()
    if not watchlist_entry:
        raise ValueError("Watchlist entry not found")
    
    if new_state not in ["To Watch", "Watched", "Watch Next"]:
        raise ValueError("New state must be 'To Watch' or 'Watched' or 'Watch Next'")
    
    if new_state == "Watched":
        delete_movie_from_watchlist(username, imdb_id)
 
    if new_state == "Watch Next":
        movie = fetch_movie_by_id(imdb_id)
        watchlist_entry.user_id = user.id
        watchlist_entry.title = movie.get('Title')
        watchlist_entry.imdb_id=movie.get('imdbID')
        watchlist_entry.year=movie.get('Year')
        watchlist_entry.rated=movie.get('Rated')
        watchlist_entry.runtime=movie.get('Runtime')
        watchlist_entry.plot=movie.get('Plot')
        watchlist_entry.genre=movie.get('Genre')
        watchlist_entry.imdb_rating=movie.get('imdbRating')
        watchlist_entry.type=movie.get('Type')
        watchlist_entry.watching_state="Watch Next" 
    
    db.session.commit()
    logger.info(f"Updated '{watchlist_entry.title}' for {username}")

def get_user_watchlist (username):
    """
    Gets all movies for a user 

    Arguments:
        username (str): The username of user.

    Raises:
        ValueError: If user is not found.
        ValueError: If user has no movies.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError("User not found")

    user_watchlist = Watchlist.query.filter_by(user_id=user.id).all()
    if len(user_watchlist) == 0:
        raise ValueError(f"No movies found in watchlist for {username}")

    user_watchlist_data = []
    for movie in user_watchlist:
        movie_data = {
            'imdbID': movie.imdb_id,
            'Title': movie.title,
            'Year': movie.year,
            'Rated': movie.rated,
            'Runtime': movie.runtime,
            'Plot': movie.plot,
            'Genre': movie.genre,
            'imdbRating': movie.imdb_rating,
            'Type': movie.type,
            'Watching State': movie.watching_state
        }
        user_watchlist_data.append(movie_data)

    return user_watchlist_data