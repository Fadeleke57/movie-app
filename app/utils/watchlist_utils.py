from app.models.user import User
from app.models.watchlist import Watchlist
from app.utils.omdb import fetch_movie_by_id
from app.utils.db import db
from app.routes.user_routes import logger


def add_movie_to_watchlist(username, imdb_id):
    """
    Adds a movie to user's watchlist.

    Arguments:
        username (str): The username of user.
        imdb_id (str): The IMDb of the movie.

    Raises:
        ValueError: If user is not found
        ValueError: If movie is not found
    """

    user = User.query.filter_by(username=username).first()
    if not user:
        return ValueError("User not found")
    
    movie = fetch_movie_by_id(imdb_id)
    if not movie:
        raise ValueError("Movie not found")
    
    watchlist = Watchlist(
        user_id = user.id,
        title = movie.get('title'),
        imdb_id=movie.get('imdb_id'),
        year=movie.get('year'),
        rated=movie.get('rated'),
        runtime=movie.get('runtime'),
        plot=movie.get('plot'),
        genre=movie.get('genre'),
        imdb_rating=movie.get('imdb_rating'),
        type=movie.get('type'),
        watching_state="To Watch" 
    )

    db.session.add(watchlist)
    db.session.commit()

    logger.info(f"Added movie '{movie.get('title')}' to {username}'s watchlist successfully.")

    
