from app.utils.db import db

class Watchlist(db.Model):
    """
    Represents a watchlist entry in the movie app.

    Attributes:
        id (int): The primary key of the watchlist entry.
        user_id (int): The ID of the user who owns the watchlist entry.
        title (str): The title of the movie or show.
        imdb_id (str): The IMDb ID of the movie or show.
        year (str, optional): The release year of the movie or show.
        rated (str, optional): The rating of the movie or show.
        runtime (str, optional): The runtime of the movie or show.
        plot (str, optional): The plot summary of the movie or show.
        genre (str, optional): The genre of the movie or show.
        imdb_rating (str, optional): The IMDb rating of the movie or show.
        type (str, optional): The type of the entry (e.g., "movie", "series").
        watching_state (str, optional): The watching state of the entry (e.g., "To Watch", "Watched", "Watch Next").
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(4))
    rated = db.Column(db.String(10))
    runtime = db.Column(db.String(20))
    plot = db.Column(db.Text)
    genre = db.Column(db.String(100))
    imdb_rating = db.Column(db.String(10))
    type = db.Column(db.String(20))
    watching_state = db.Column(db.String(20))  # e.g., "To Watch", "Watched", "Watch Next"
