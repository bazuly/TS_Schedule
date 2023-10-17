from fastapi import APIRouter, HTTPException, Depends, Query
from schema import Driver_data as schema_driver_data
from models import Driver_data as model_driver_data
from fastapi_sqlalchemy import db
from config import get_db
from sqlalchemy.orm import Session

router = APIRouter()
""" Post data"""


@router.post('/add_driver_data', response_model=schema_driver_data)
async def add_driver_data(driver_data_add: schema_driver_data):
    try:
        db_add_driver_data = model_driver_data(
            name=driver_data_add.name.lower(),
            other=driver_data_add.other.lower()
            if driver_data_add.other else None,
            phone_number=driver_data_add.phone_number.lower()
            if driver_data_add.phone_number else None)
        db.session.add(db_add_driver_data)
        db.session.commit()

        return db_add_driver_data

    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Get data """

# и инфу все равно выдавало, например если фамилия уникальная, то только по фамилии
# или найти всех водителей с именем Александр


@router.get('/get_driver_data')
async def get_driver_data_from_db(name: str = Query(None,
                                                    description='Driver Name'),
                                  limit: int = Query(None,
                                                     description='Limit',
                                                     le=1000),
                                  db: Session = Depends(get_db)):
    query = db.query(model_driver_data.name, model_driver_data.other,
                     model_driver_data.phone_number)
    try:
        if name:
            query = query.filter(
                model_driver_data.name == name.lower().split())

        query = query.limit(limit)

        driver_data = query.all()

        if driver_data is None:
            raise HTTPException(status_code=404,
                                detail='Driver data not found')

        driver_data_dicts = [
            dict((key, value.lower()) for key, value in row._asdict().items())
            for row in driver_data
        ]

        return driver_data_dicts

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Delete Data """


@router.delete('/delete_driver_data')
async def delete_driver_data(name: str = Query(None,
                                               description='Driver name',
                                               alias='driver_name'),
                             other: str = Query(None,
                                                description='Other data'),
                             phone_number: str = Query(
                                 None, description='Phone number'),
                             db: Session = Depends(get_db)):

    try:
        driver_data_query = db.query(model_driver_data).filter(
            model_driver_data.name == name.lower().split())

        if not driver_data_query:
            raise HTTPException(status_code=404,
                                detail='Driver data not found')

        for driver_data in driver_data_query:
            db.delete(driver_data)

        db.commit()

        return {'message': 'Driver data deleted succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Patch Data """


@router.patch('/update_driver_data')
async def update_driver_data(
        name: str = Query(None, description='Driver Name',
                          alias='driver_name'),
        new_name: str = Query(None, description='Update name'),
        new_data: str = Query(None, description='Update driver data'),
        new_phone_number: str = Query(None, description='Update phone number'),
        db: Session = Depends(get_db)):

    try:
        driver_data_query = db.query(model_driver_data).filter(
            model_driver_data.name == name.lower().split()).first()

        if not driver_data_query:
            raise HTTPException(status_code=404,
                                detail='Driver data not found')

        if new_name is not None:
            driver_data_query.name = new_name

        if new_data is not None:
            driver_data_query.other = new_data

        if new_phone_number is not None:
            driver_data_query.phone_number = new_phone_number


        db.commit()

        return {'message': 'Data updated succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')
