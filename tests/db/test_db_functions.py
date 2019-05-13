import pytest
from unittest.mock import patch, Mock
from db.db_functions import get_restaurant_by_ratings
import datetime
from sqlalchemy import Column

class TestDBFunctions(object):
    # NOTE: Unfortunately, this test does not pass. Was not able to figure out how to mock session.description
    @patch('db.db_functions.psycopg2.connect')
    @patch('db.db_functions.DBRestaurantQuery')
    def test_get_restaurant_by_ratings(self, mock_db_rest_query, mock_conn):
        mock_db_rest_query.get_restaurants.return_value = Mock()
        mock_db_rest_query.with_ratings_filter.return_value = Mock()
        mock_db_rest_query.with_cuisine_filter.return_value = Mock()

        mock_conn.return_value.cursor.return_value.execute = Mock()
        mock_conn.return_value.cursor.return_value.fetchall.return_value = _get_results()
        # this line below should actually be: mock_conn.return_value.cursor.return_value.description = _get_session_desc()
        mock_conn.return_value.cursor.return_value.description.return_value = _get_session_desc()

        ratings = ['B']
        cuisine = 'American'

        # When
        results = get_restaurant_by_ratings(ratings, cuisine)

        # Then
        assert type(results) == list
        assert results[0]['cuisine'] == cuisine

    @patch('db.db_functions.psycopg2.connect')
    @patch('db.db_functions.DBRestaurantQuery')
    def test_get_restaurant_by_ratings_wheh_db_error(self, mock_db_rest_query, mock_conn):
        mock_db_rest_query.get_restaurants.return_value = Mock()
        mock_db_rest_query.with_ratings_filter.return_value = Mock()
        mock_db_rest_query.with_cuisine_filter.return_value = Mock()

        mock_conn.return_value.cursor.side_effect = Exception("Error querying database.")

        ratings = ['B']
        cuisine = 'American'
        # When
        with pytest.raises(Exception) as excinfo:
            get_restaurant_by_ratings(ratings, cuisine)

def _get_results():
    return [['CHARLEY ST', 'MANHATTAN', '41', 'KENMARE ST', '10012.0', '+218083046662', 'American', 'A', datetime.date(2018, 9, 14)]]


def _get_session_desc():
    return (Column(name='name', display_size=None),
            Column(name='borough', display_size=None),
            Column(name='building', display_size=None), 
            Column(name='street', display_size=None), 
            Column(name='zipcode', display_size=None),
            Column(name='phone', display_size=None), 
            Column(name='cuisine', display_size=None), 
            Column(name='grade', display_size=None), 
            Column(name='inspection_date', display_size=None))


