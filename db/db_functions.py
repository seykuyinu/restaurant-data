
import psycopg2
from psycopg2.extras import DictCursor
from db.db_query import DBRestaurantQuery
from os import environ

DATABASE_URL = environ['DATABASE_URL']
all_ratings = ['N', 'A', 'B', 'C', 'Z', 'P']

def get_restaurant_by_ratings(ratings: list = all_ratings, cuisine:str=None):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
    
    except Exception as e:
        raise e