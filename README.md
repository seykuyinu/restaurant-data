# Restaurant Data

## Submission Information
### Hosted app

https://sey-restaurant-data.herokuapp.com/restaurants

### File list:
* [DB Schema Explanation](schema.md)
* [ETL Job](etl/etl_job.py)
* [API Code](api.py)
* [SQL Query](queries.sql)
* [CURL request](curl_request.sh)

## Local Setup

Python version 3.6+ - Recommend using a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/)

```pip install -r requirements.txt etl/requirements.txt```

### Run ETL job
1. Configure the database url for Postgres and set as the environment variable `DATABASE_URL`: 
```bash
export DATABASE_URL=postgres://username:password@host:port/database_name
```
2. Copy the CSV file to the `etl` folder, and set the `CSV_FILENAME` variable in `etl/variables.py`.

3. Run the ETL job
```bash
python etl/etl_job.py
```

### Start API

From the root directory, run: 
```bash
bash start_app.sh
```

API endpoint will be: localhost:5000/restaurants

### Run unit tests
```bash
pytest tests
```
