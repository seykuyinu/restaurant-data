
import psycopg2
from psycopg2.extras import DictCursor
from restaurants.db_query import DBRestaurantQuery
from os import environ

db_name = environ['DB_NAME']
db_username = environ['DB_USERNAME']
# db_password = environ['DB_PASSWORD']

def get_restaurant_by_ratings(ratings: list, cuisine:str=None):
    try:
        conn = psycopg2.connect(host="localhost", port="5432", dbname=db_name, user=db_username)
        session = conn.cursor(cursor_factory = DictCursor)

        db_query = DBRestaurantQuery().get_restaurants().with_ratings_filter(ratings)

        if cuisine:
            db_query.with_cuisine_filter(cuisine)

        session.execute(db_query.query)
        results = session.fetchall()

        desc = session.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))  
            for row in  results]
        
        session.close()
        conn.close()

        return data
    
    except Exception:
        # log
        raise