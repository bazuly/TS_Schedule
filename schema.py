from pydantic import BaseModel
from datetime import date

class Document_create(BaseModel):
    title: str

    # class Config:
    #     orm_mode = True

class Document_response(BaseModel):
    id: int
    title: str

    # class Config:
    #     orm_mode = True

class Driver_data(BaseModel):
    name: str
    other: str = None
    phone_number: str = None

    class Config:
        orm_mode = True


class Car_add(BaseModel):
    car_number: str
    trailer_number: str = None
    brand: str = None
    load_capacity: str = None


    class Config:
        orm_mode = True


class Driver_salary(BaseModel):
    name: str
    salary_amount: float
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


class Driver_penalty(BaseModel):
    name: str
    penalty_amount: int
    penalty_cause: str = None
    penalty_date: date

    class Config:
        orm_mode = True


class Travel_allowances(BaseModel):
    name: str
    travel_allowances: int
    amount_of_days: int
    start_date: date
    end_date: date


    class Config:
        orm_mode = True
