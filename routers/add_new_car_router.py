from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_sqlalchemy import db
from models import Car_add as model_car_add
from schema import Car_add as schema_car_Add
from config import get_db
from sqlalchemy.orm import Session


router = APIRouter()

""" Post data """


@router.post('/add_new_car', response_model=schema_car_Add)
async def add_new_car(car_add: schema_car_Add) -> str:
    try:
        db_new_car = model_car_add(
            car_number=car_add.car_number.lower(),
            trailer_number=car_add.trailer_number.lower()
            if car_add.trailer_number else None,
            brand=car_add.brand.lower() if car_add.brand else None,
            load_capacity=car_add.load_capacity.lower()
            if car_add.load_capacity else None)
        db.session.add(db_new_car)
        db.session.commit()

        return db_new_car

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Get data """

# set limit get data
@router.get('/get_car')
async def get_car_from_db(
        car_id: int = Query(None, description="Car ID", alias="id"),
        car_number: str = Query(None, description="Car Number"),
        trailer_number: str = Query(None, description="Trailer Number"),
        brand: str = Query(None, description="Car Brand"),
        load_capacity: str = Query(None, description="Load Capacity"),
        db: Session = Depends(get_db)):

    try:
        query = db.query(model_car_add.car_number,
                         model_car_add.trailer_number,
                         model_car_add.brand,
                         model_car_add.load_capacity)

        if car_id:
            query = query.filter(model_car_add.id == car_id)

        if car_number:
            query = query.filter(model_car_add.car_number == car_number.lower().split())

        if trailer_number:
            query = query.filter(model_car_add.trailer_number == trailer_number.lower().split())

        if brand:
            query = query.filter(model_car_add.brand == brand.lower().split())

        if load_capacity:
            query = query.filter(model_car_add.load_capacity == load_capacity.lower().split())

        car_data = query.all()

        if car_data is None:
            raise HTTPException(status_code=404, detail="Car not found")

        car_data_dicts =[
            dict((key, value.lower()) for key, value in row._asdict().items())
            for row in car_data
        ]


        return car_data_dicts

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Delet data """

@router.delete('/delete_car_data')
async def delete_car_data(car_number: str = Query(None,
                                                    description='Car number'),
                          db: Session = Depends(get_db)):

    try:
        car_data_query = db.query(model_car_add).filter(
            model_car_add.car_number == car_number.lower().split()
        )

        if not car_data_query:
            raise HTTPException(status_code=404,
                                detail='Car data not found')

        for car_data in car_data_query:
            db.delete(car_data)

        db.commit()

        return {'message': 'Message deleted succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')
