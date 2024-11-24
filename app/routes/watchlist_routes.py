from flask import Blueprint, request, jsonify
import requests
import os
from app.routes.user_routes import logger
from app.models.user import User
from app.utils.watchlist_utils import (
    add_movie_to_watchlist
)

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    """
    Route to create a new watchlist for a user.
    
    Expects JSON Input:
        - username(str): username of user
        - imdb_id(str): IMDb ID of movie
    
    Returns:
        JSON response indicating the success of creating a new watchlist.

    Raises:
        400 error if invalid input
        404 error if username not found
        500 error if unexcepted error occurred
    """
    logger.info("Adding to watchlist")
    
    try:
        data = request.get_json()
        username = data.get('username')
        imdb_id = data.get('imdb_id')

        #check if valid input
        if not username or not imdb_id:
            return jsonify({'error': 'Username and imdb_id required'}), 400

         #check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        #add movie to watchlist 
        add_movie_to_watchlist(username=username, imdb_id=imdb_id)
        logger.info(f"Movie {imdb_id} added to {username}'s watchlist")
        return jsonify({"message": f"Movie added to {username}'s watchlist"}), 201
        
    # Handle unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

        