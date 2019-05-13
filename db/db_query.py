class DBRestaurantQuery:
    def __init__(self):
        self.query = ""

    def get_restaurants(self):
        self.query = """SELECT restaurant_info.name, restaurant_info.borough, restaurant_info.building, restaurant_info.street, 
                    restaurant_info.zipcode, restaurant_info.phone, restaurant_info.cuisine, 
                    inspection_info.grade, inspection_info.inspection_date 
                    FROM restaurant_info INNER JOIN inspection_info 
                    ON restaurant_info.id = inspection_info.id"""
        return self

    def with_ratings_filter(self, ratings: list):
        if len(ratings) > 1:
            ratings = tuple(ratings)
        else:
            ratings = f"(\'{ratings[0]}\')"

        rating_query = f"WHERE grade in {ratings}"
        self.query = self.query + f" {rating_query}"
        return self

    def with_cuisine_filter(self, cuisine: str):
        cuisine_query = f"AND cuisine = \'{cuisine}\'"
        self.query = self.query + f" {cuisine_query}"
        return self
        
    def get_query(self):
       return self.query