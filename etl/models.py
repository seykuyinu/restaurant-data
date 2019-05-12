from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey

Base = declarative_base()

class RestaurantInfo(Base):
    __tablename__ = 'restaurant_info'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))
    borough = Column(String(255))
    building = Column(String(255))
    street = Column(String(255))
    zipcode = Column(String(20))
    phone = Column(String(50))
    cuisine = Column(String(255))
    

class InspectionInfo(Base):
    __tablename__ = 'inspection_info'
    id = Column(Integer,  ForeignKey('restaurant_info.id'), primary_key=True)
    inspection_date = Column(Date)
    action = Column(Text)
    violation_code = Column(String(255))
    violation_desc = Column(Text)
    critical_flag = Column(String(255))
    score = Column(Float)
    grade = Column(String(255))
    grade_date = Column(Date)
    record_date = Column(Date)
    inspection_type = Column(String(255))