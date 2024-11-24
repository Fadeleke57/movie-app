from flask import Blueprint, request, jsonify
import requests
from app.utils.logger import logger
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the app is running.
    """
    logger.info("Health check")
    return jsonify({"status": "App is running!"}), 200
