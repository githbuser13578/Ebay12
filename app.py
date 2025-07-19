from flask import Flask, jsonify, request, redirect
import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# eBay API credentials
EBAY_APP_ID = "GilesCle-A-SBX-f0bb589a9-f66214b5"
EBAY_DEV_ID = "9c190ab3-af18-458d-9d8c-49a4c10ddaea4"
EBAY_CERT_ID = "SBX-0bb589a9da6c-631f-4849-94b0-ee43"
EBAY_REDIRECT_URI = "https://ebay12.onrender.com/callback"

# eBay API URL for finding listings
EBAY_API_URL = "https://svcs.ebay.com/services/search/FindingService/v1"

# OAuth2 credentials encoding for Authorization header
credentials = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Home Route
@app.route('/')
def index():
    return "Welcome to the eBay Relister!"

# Fetch Listings Route
@app.route('/fetch_listings', methods=['GET'])
def fetch_listings():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required!"}), 400

    params = {
        'OPERATION-NAME': 'findItemsByKeywords',
        'SERVICE-VERSION': '1.0.0',
        'SECURITY-APPNAME': EBAY_APP_ID,
        'GLOBAL-ID': 'EBAY-US',
        'keywords': query,
        'paginationInput.entriesPerPage': '5'
    }

    response = requests.get(EBAY_API_URL, params=params)
    return jsonify(response.json())

# OAuth Authorization Route
@app.route('/authorize')
def authorize():
    auth_url = f"https://auth.sandbox.ebay.com/oauth2/authorize?client_id={EBAY_APP_ID}&redirect_uri={EBAY_REDIRECT_URI}&response_type=code&scope=https://api.ebay.com/oauth/api_scope"
    return redirect(auth_url)

# Callback Route for OAuth
@app.route('/callback')
def callback():
    # Get the authorization code from eBay's response
    code = request.args.get('code')

    if not code:
        return jsonify({"error": "Missing authorization code!"}), 400

    # Prepare data for token exchange
    token_url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': EBAY_REDIRECT_URI
    }

    # Request token from eBay
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'  # Base64 encoded client_id:client_secret
    }

    # Sending token request
    token_response = requests.post(token_url, data=data, headers=headers)
    token_data = token_response.json()

    if 'access_token' in token_data:
        # Access token obtained, send it as a response
        return jsonify({"access_token": token_data['access_token']})
    else:
        return jsonify({"error": "Failed to obtain access token!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
