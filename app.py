
import requests
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Set your eBay API credentials
EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_DEV_ID = os.getenv("EBAY_DEV_ID")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")

# Fetch listings from eBay using the Finding API
@app.route("/fetch_listings", methods=["GET"])
def fetch_listings():
    query = request.args.get("query", "laptop")  # Default search for 'laptop'
    ebay_url = f"https://svcs.ebay.com/services/search/FindingService/v1"
    
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "keywords": query,
        "paginationInput.entriesPerPage": 5,
        "responseDataFormat": "JSON"
    }

    response = requests.get(ebay_url, params=params)
    items = response.json().get('findItemsByKeywordsResponse', [])[0].get('searchResult', [])[0].get('item', [])

    listings = []
    for item in items:
        title = item.get('title', ['No Title'])[0]
        price = item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('__value__', 'N/A')
        url = item.get('viewItemURL', ['N/A'])[0]
        
        listings.append({
            "title": title,
            "price": price,
            "url": url
        })
    
    return jsonify(listings)

# Relist an item with a price markup using eBay's Trading API
@app.route("/relist_item", methods=["POST"])
def relist_item():
    data = request.json
    title = data["title"]
    price = float(data["price"])
    markup_price = price * 1.10  # Example: 10% markup

    ebay_url = "https://api.ebay.com/ws/api.dll"
    
    headers = {
        "X-EBAY-API-APP-ID": EBAY_APP_ID,
        "X-EBAY-API-DEV-ID": EBAY_DEV_ID,
        "X-EBAY-API-CERT-ID": EBAY_CERT_ID,
        "X-EBAY-API-CALL-NAME": "AddItem",
        "Content-Type": "text/xml"
    }
    
    request_body = '''<?xml version="1.0" encoding="utf-8"?>
    <AddItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <ErrorLanguage>en_US</ErrorLanguage>
        <RequesterCredentials>
            <eBayAuthToken>YourAuthTokenHere</eBayAuthToken>
        </RequesterCredentials>
        <Item>
            <Title>{}</Title>
            <Description>This is a resold item.</Description>
            <PrimaryCategory>
                <CategoryID>12345</CategoryID>
            </PrimaryCategory>
            <StartPrice>{}</StartPrice>
            <ConditionID>1000</ConditionID>
            <CategoryMappingAllowed>false</CategoryMappingAllowed>
            <Location>US</Location>
            <Country>US</Country>
            <Currency>USD</Currency>
            <ListingDuration>GTC</ListingDuration>
            <ShippingDetails>
                <ShippingServiceOptions>
                    <ShippingService>USPSMedia</ShippingService>
                    <ShippingServiceCost>5.00</ShippingServiceCost>
                </ShippingServiceOptions>
            </ShippingDetails>
        </Item>
    </AddItemRequest>'''.format(title, markup_price)

    response = requests.post(ebay_url, headers=headers, data=request_body)
    return jsonify({"message": "Item relisted successfully!"}) if response.status_code == 200 else jsonify({"error": "Failed to relist item"})

if __name__ == "__main__":
    app.run(debug=True)
