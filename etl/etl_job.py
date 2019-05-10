import pandas as pd
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, RestaurantInfo, InspectionInfo

path = os.path.join('restaruants_subset.csv')
# path = os.path.join('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
restaurant_data = pd.read_csv(path, dtype={'PHONE': object})

# move out?
column_rename_mapping = {
    "CAMIS" : "id",
    "DBA" : "name",
    "BORO" : "borough",
    "CUISINE DESCRIPTION" : "cuisine",
    "INSPECTION DATE" : "inspection_date",
    "VIOLATION CODE" : "violation_code",
    "VIOLATION DESCRIPTION" : "violation_desc",
    "CRITICAL FLAG" : "critical_flag",
    "GRADE DATE" : "grade_date",
    "RECORD DATE" : "record_date",
    "INSPECTION TYPE" : "inspection_type"
}

REST_INFO_COLUMNS = ["id", "name", "borough", "building", "street", "zipcode", "phone","cuisine"]
DATE_COLUMNS = ["inspection_date", "grade_date", "record_date"]

# all NaN fields in grade to None

# transform phone numbers? add 0 or dialing code?

restaurant_data.rename(columns=column_rename_mapping, inplace=True)
restaurant_data = restaurant_data.rename(str.lower, axis="columns")

# TODO: format??!!!!
restaurant_data[DATE_COLUMNS] = restaurant_data[DATE_COLUMNS].apply(pd.to_datetime)

# get ids for each restaurant
list_ids = restaurant_data['id'].drop_duplicates()

rest_info_rows = [] 
inspection_info_rows = []
    
# get all rows satisfying the id from rest_info
for restaurant_id in list_ids:
    restaurant = restaurant_data.loc[restaurant_data['id'] == restaurant_id]
    restaurant_info = restaurant.loc[:, REST_INFO_COLUMNS]
    restaurant_info = restaurant_info.iloc[0]

    # what is this doing?
    restaurant = restaurant.drop(REST_INFO_COLUMNS[1:], axis=1)

    # get latest inspection, add to inspection dataframe
    restaurant = restaurant.sort_values(['grade_date'], axis=0, ascending=False)
    most_recent_grading = restaurant.iloc[0]
    
    add_row_to_list(restaurant_info, rest_info_rows)
    add_row_to_list(most_recent_grading, inspection_info_rows)

restaurant_info_df = pd.DataFrame(rest_info_rows)
inspection_info_df = pd.DataFrame(inspection_info_rows)

engine = create_engine('postgres+psycopg2://seykuyinu@localhost:5432/seykuyinu')
write_df_to_db(engine, restaurant_info_df, RestaurantInfo)
write_df_to_db(engine, inspection_info_df, InspectionInfo)

# print(restaurant_info_df.loc[0])

def write_df_to_db(engine, df, model):
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_insert_mappings(model, df.to_dict(orient="records"))
    session.commit()
    session.close()

    # Session = sessionmaker(bind=engine)
    # session = Session()
    # session.bulk_insert_mappings(InspectionInfo, inspection_info_df.to_dict(orient="records"))
    # session.commit()
    # session.close()


# seems to work
def add_row_to_list(row: pd.Series, list_to_update: list):
    temp_dict = {}
#   need to add to_dict or implicitly does conversion?
    temp_dict.update(row.to_dict())
    list_to_update.append(temp_dict)