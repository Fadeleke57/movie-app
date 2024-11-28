# Description: Routes for user account creation.
from flask import Blueprint, request, jsonify
from app.utils.logger import logger
from app.models.user import User
from app.utils.db import db
from app.utils.hashing import hash_password
from app.utils.hashing import verify_password
user_bp = Blueprint('user', __name__)
# Configure logger

user_bp = Blueprint('user', __name__)

@user_bp.route('/create-account', methods=['POST'])
def create_account():
    """
    Route to create a new user account.
    Expects JSON data with 'username' and 'password'.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        logger.info('Username and password are required')
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        logger.info(f'Username already exists: {username}')
        return jsonify({'error': 'Username already exists'}), 409

    # Hash the password
    salt, hashed_password = hash_password(password)

    # Create a new user
    new_user = User(username=username, salt=salt, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    logger.info(f'New account created: {username}')
    return jsonify({'message': 'Account created successfully'}), 201



@user_bp.route('/login', methods=['POST'])
def login():
    """
    Route to log in a user.
    Expects JSON data with 'username' and 'password'.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Retrieve user from database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Verify the password
    if verify_password(user.salt, user.hashed_password, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@user_bp.route('/update-password', methods=['POST'])
def update_password():
    """
    Route to update a user's password.
    Expects JSON data with 'username', 'old_password', and 'new_password'.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not username or not old_password or not new_password:
        return jsonify({'error': 'Username, old password, and new password are required'}), 400

    # Retrieve user from database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify the old password
    if not verify_password(user.salt, user.hashed_password, old_password):
        return jsonify({'error': 'Old password is incorrect'}), 401

    # Hash the new password
    salt, hashed_password = hash_password(new_password)

    # Update the user's password
    user.salt = salt
    user.hashed_password = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200