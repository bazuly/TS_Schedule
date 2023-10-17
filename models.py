from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, LargeBinary

Base = declarative_base()

class Document_data(Base):
    __tablename__ = 'document_data'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    file_data = Column(LargeBinary)

class Driver_data(Base):
    __tablename__ = 'driver_data'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    other = Column(String, index=True)
    phone_number = Column(String, index=True)


class Car_add(Base):
    __tablename__ = 'add_car_data'

    id = Column(Integer, primary_key=True, index=True)
    car_number = Column(String, index=True, nullable=False)
    trailer_number = Column(String, index=True)
    brand = Column(String, index=True)
    load_capacity = Column(String, index=True)


class Driver_salary(Base):
    __tablename__ = 'driver_salary'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    salary_amount = Column(Float, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)


class Driver_penalty(Base):
    __tablename__ = 'driver_penalty'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    penalty_amount = Column(Integer, index=True)
    penalty_cause = Column(String, index=True)
    penalty_date = Column(Date, index=True)


class Travel_allowances(Base):
    __tablename__ = 'travel_allowances'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    travel_allowances = Column(Integer, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date)
    amount_of_days = Column(Integer, index=True)
