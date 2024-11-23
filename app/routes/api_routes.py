from flask import Blueprint, request, jsonify
import requests
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the app is running.
    """
    return jsonify({"status": "App is running!"}), 200
