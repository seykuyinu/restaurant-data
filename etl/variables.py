REST_INFO_COLUMNS = ["id", "name", "borough", "building", "street", "zipcode", "phone","cuisine"]
DATE_COLUMNS = ["inspection_date", "grade_date", "record_date"]
NEW_YORK_DIAL_CODE = '21'
COLUMN_RENAME_MAPPING = {
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