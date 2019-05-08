-- Main SQL query to fulfil friend's dining requirement

SELECT restaurant_info.name, restaurant_info.borough, restaurant_info.building, restaurant_info.street, restaurant_info.zipcode, restaurant_info.phone, restaurant_info.cuisine, inspection_info.grade, inspection_info.inspection_date
FROM restaurant_info INNER JOIN inspection_info
ON restaurant_info.id = inspection_info.id
WHERE (grade = 'A' OR grade = 'B')
AND cuisine = 'Thai';

-- SQL queries used for testing. Before the use of sqlalchemy

CREATE DATABASE restaurant_inspections

CREATE TABLE restaurant_info (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    borough VARCHAR(255),
    building VARCHAR(255),
    street VARCHAR(255),
    zipcode VARCHAR(10),
    phone VARCHAR(15),
    cuisine VARCHAR(255)
);

CREATE TABLE inspection_info (
    id INT PRIMARY KEY,
    inspection_date DATE,
    action TEXT,
    violation_code VARCHAR(255),
    violation_desc TEXT,
    critical_flag VARCHAR(255),
    score REAL,
    grade CHAR(1),
    grade_date DATE,
    record_date DATE,
    inspection_type VARCHAR(255),
    FOREIGN KEY (id) REFERENCES restaurant_info(id)
);