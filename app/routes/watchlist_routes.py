from flask import Blueprint, request, jsonify
import requests
import os
from app.routes.user_routes import logger
from app.models.user import User
from app.utils.watchlist_utils import (
    add_movie_to_watchlist,
    delete_movie_from_watchlist,
    update_movie_from_watchlist,
    get_user_watchlist
)

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/add-to-watchlist', methods=['POST'])
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
        
    #Handle unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

@watchlist_bp.route('/delete-from-watchlist', methods=['DELETE'])
def delete_from_watchlist():
    """
    Route to delete a watchlist for a user.
    
    Expects JSON Input:
        - username(str): username of user
        - imdb_id(str): IMDb ID of movie
    
    Returns:
        JSON response indicating the success of deleting a watchlist.

    Raises:
        400 error if invalid input
        404 error if username not found
        500 error if unexcepted error occurred
    """
    logger.info("Deleting from watchlist")
    
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

        #delete movie to watchlist 
        delete_movie_from_watchlist(username=username, imdb_id=imdb_id)
        logger.info(f"Movie {imdb_id} deleted from {username}'s watchlist")
        return jsonify({"message": f"Movie deleted from {username}'s watchlist"}), 200
        
    #Handle unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@watchlist_bp.route('/update-watchlist', methods=['PUT'])
def update_watchlist():
    """
    Route to update a watchlist for a user.
    
    Expects JSON Input:
        - username(str): username of user
        - imdb_id(str): IMDb ID of movie
        - watching_state(str): watching state is either 'To Watch' or 'Watched' or 'Watch Next'
    
    Returns:
        JSON response indicating the success of deleting a watchlist.

    Raises:
        400 error if invalid input
        404 error if username not found
        404 error if watching state not 'To Watch' or 'Watched' or 'Watch Next'
        500 error if unexcepted error occurred
    """
    logger.info("Updating watchlist")
    
    try:
        data = request.get_json()
        username = data.get('username')
        imdb_id = data.get('imdb_id')
        watching_state = data.get('watching_state')

        #check if valid input
        if not username or not imdb_id or not watching_state:
            return jsonify({'error': 'Username, imdb_id, and watching_state required'}), 400

        #check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        #check if watching state is not 'To Watch' or 'Watched' or 'Watch Next'
        if watching_state not in ["To Watch", "Watched", "Watch Next"]:
            return jsonify({'error': 'Watching state must be "To Watch" or "Watched" or "Watch Next"'}), 404

        #update movie in watchlist 
        update_movie_from_watchlist(username=username, imdb_id=imdb_id, new_state=watching_state)
        logger.info(f"Movie {imdb_id} updated from {username}'s watchlist")
        return jsonify({"message": f"Movie updated from {username}'s watchlist"}), 200
        
    #Handle unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@watchlist_bp.route('/get-watchlist', methods=['GET'])
def get_watchlist():    
    """
    Route to get a watchlist for a user.
    
    Expects JSON Input:
        - username(str): username of user
     
    Returns:
        JSON response indicating the success of getting user watchlist.

    Raises:
        400 error if invalid input
        404 error if username not found
        500 error if unexcepted error occurred
    """
    logger.info("Getting watchlist")
    
    try:
        data = request.get_json()
        username = data.get('username')

    #check if valid input
        if not username :
            return jsonify({'error': 'Username required'}), 400

    #check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
    #Get user watchlist
        user_watchlist = get_user_watchlist(username)
        logger.info(f"Got {username}'s watchlist")
        return jsonify({"message": f"{username}'s watchlist", "watchlist": user_watchlist}), 200


    #Handle unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
