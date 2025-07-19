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

