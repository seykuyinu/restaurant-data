import pandas as pd
import os 
from sqlalchemy import create_engine
from models import Base, RestaurantInfo, InspectionInfo
from variables import REST_INFO_COLUMNS, INSPECITON_INFO_COLUMNS, DATE_COLUMNS, NEW_YORK_DIAL_CODE, COLUMN_RENAME_MAPPING, CSV_FILENAME, DATABASE_URL
import io

def transform_data(df: pd.DataFrame):
    df.rename(columns=COLUMN_RENAME_MAPPING, inplace=True)
    df = df.rename(str.lower, axis="columns")
    
    # Transform phone numbers, date
    df['phone'] = df['phone'].apply(lambda x: 0 if pd.isnull(x) else f'+{NEW_YORK_DIAL_CODE}{x}')
    df[DATE_COLUMNS] = df[DATE_COLUMNS].apply(pd.to_datetime)
    
    return df

def write_df_to_db(engine, df:pd.DataFrame, model):
    try:
        Base.metadata.create_all(engine)

        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        cur.copy_from(output, model.__tablename__, null="") # null values become ''
        conn.commit()
        conn.close()

    except Exception:
        raise


def add_row_to_list(row: pd.Series, list_to_update: list):
    temp_dict = {}
    temp_dict.update(row.to_dict())
    list_to_update.append(temp_dict)


def process(restaurant_data: pd.DataFrame):
    # get ids for each restaurant
    list_ids = restaurant_data['id'].drop_duplicates()

    rest_info_rows = [] 
    inspection_info_rows = []
        
    # get all rows satisfying the id from rest_info
    for restaurant_id in list_ids:
        restaurant = restaurant_data.loc[restaurant_data['id'] == restaurant_id]
        restaurant_info = restaurant.loc[:, REST_INFO_COLUMNS]
        # only need one row as 'information' columns are the same
        restaurant_info = restaurant_info.iloc[0]

        # Remove the restaurant information related columns, leave inspection related columns
        restaurant = restaurant.drop(REST_INFO_COLUMNS[1:], axis=1)
        # get latest inspection details
        restaurant = restaurant.sort_values(['grade_date'], axis=0, ascending=False)
        most_recent_grading = restaurant.iloc[0]
       
        add_row_to_list(restaurant_info, rest_info_rows)
        add_row_to_list(most_recent_grading, inspection_info_rows)

    # convert lists to dfs
    restaurant_info_df = pd.DataFrame(rest_info_rows)
    inspection_info_df = pd.DataFrame(inspection_info_rows)

    return restaurant_info_df, inspection_info_df

def main():
    transformed_restaurant_data = pd.DataFrame()
    chunksize = 1000
    path = os.path.join(CSV_FILENAME)

    print('Reading csv file..')
    restaurant_data = pd.read_csv(path, dtype={'PHONE': object}, chunksize=chunksize)
    for chunk in restaurant_data:
        transformed_data_tmp = transform_data(chunk)
        transformed_restaurant_data = transformed_restaurant_data.append(transformed_data_tmp)

    print('Processing the data..')
    restaurant_info_df, inspection_info_df = process(transformed_restaurant_data)

    # arrange columns
    restaurant_info_df = restaurant_info_df[REST_INFO_COLUMNS]
    inspection_info_df = inspection_info_df[INSPECITON_INFO_COLUMNS]

    engine = create_engine(DATABASE_URL)
    print('Writing dataframes to database.. ')
    write_df_to_db(engine, restaurant_info_df, RestaurantInfo)
    write_df_to_db(engine, inspection_info_df, InspectionInfo)
    
if __name__ == "__main__":
    main()