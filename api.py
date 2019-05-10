from flask import Flask, request, jsonify, Response
from restaurants.db_functions import get_restaurant_by_ratings
import logging

CUISINE_KEY = 'cuisine'
RATINGS_KEY = 'rating'

app = Flask(__name__)

logger = logging.getLogger()

# add logging

@app.route('/restaurants', methods=['GET'])
def get_req():
    cuisine = request.args.get(CUISINE_KEY)
    ratings = request.args.getlist(RATINGS_KEY)

    try:
        results = get_restaurant_by_ratings(ratings, cuisine=cuisine)
        print(results)
        logger.info(f"Results: {results}")
        # response = Response(jsonify(results), status=200, mimetype='application/json')
        response = jsonify(results)
    except Exception as e:
        logger.exception("Error")
        response = Response(status=400, mimetype='application/json')
    
    return response


if __name__ == "__main__":
    app.run()