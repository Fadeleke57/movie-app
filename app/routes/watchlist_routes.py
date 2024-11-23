from flask import Blueprint, request, jsonify
import requests
import os

watchlist_bp = Blueprint('watchlist', __name__)