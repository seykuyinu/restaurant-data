from flask import Flask, request, jsonify, Response
from db.db_functions import get_restaurant_by_ratings
import logging

CUISINE_KEY = 'cuisine'
RATINGS_KEY = 'rating'

app = Flask(__name__)

@app.route('/restaurants', methods=['GET'])
def get_req():
    cuisine = request.args.get(CUISINE_KEY)
    ratings = request.args.getlist(RATINGS_KEY)

    try:
        results = get_restaurant_by_ratings(ratings, cuisine=cuisine)
        response = jsonify(results)
    except Exception as e:
        app.logger.error(f"Error getting restaurant information: {e}")
        response = Response(status=400, mimetype='application/json')
    
    return response


if __name__ == "__main__":
    app.run()