from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the app instance is created
app = Flask(__name__)

EBAY_APP_ID = os.getenv("GilesCle-A-SBX-f0bb589a9a6c-631f-4849-94b0-f66214b5")
EBAY_DEV_ID = os.getenv("9c190ab3-af18-458d-9d8c-49a4c10dea4")
EBAY_CERT_ID = os.getenv("SBX-0bb589a9da6c-631f-4849-94b0-ee43")

EBAY_API_URL = "https://svcs.ebay.com/services/search/FindingService/v1"

@app.route('/')
def index():
    return "Welcome to the eBay Relister!"

@app.route('/fetch_listings', methods=['GET'])
def fetch_listings():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required!"}), 400

    # Mock data for testing (replace with actual eBay data later)
    mock_data = [
        {
            "title": "Example Item 1",
            "price": "10.99",
            "imageUrl": "https://via.placeholder.com/200"
        },
        {
            "title": "Example Item 2",
            "price": "20.99",
            "imageUrl": "https://via.placeholder.com/200"
        },
        {
            "title": "Example Item 3",
            "price": "30.99",
            "imageUrl": "https://via.placeholder.com/200"
        }
    ]

    # Return mock data
    return jsonify(mock_data)


