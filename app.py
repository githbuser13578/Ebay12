from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EBAY_APP_ID="GilesCle-A-SBX-f0bb589a9-f66214b5"
EBAY_DEV_ID="9c190ab3-af18-458d-9d8c-49a4c10ddaea4"
EBAY_CERT_ID="SBX-0bb589a9da6c-631f-4849-94b0-ee43"
EBAY_REDIRECT_URI="https://ebay12.onrender.com/callback"



EBAY_API_URL = "https://svcs.ebay.com/services/search/FindingService/v1"

@app.route('/')
def index():
    return "Welcome to the eBay Relister!"

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
        'paginationInput.entriesPerPage': '5',
    }

    response = requests.get(EBAY_API_URL, params=params)
    data = response.json()

    items = []
    if "findItemsByKeywordsResponse" in data:
        for item in data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
            items.append({
                'title': item['title'][0],
                'viewItemURL': item['viewItemURL'][0],
                'sellingStatus': item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                'galleryURL': item['galleryURL'][0]
            })

    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)
