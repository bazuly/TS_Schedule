from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_sqlalchemy import db
from models import Travel_allowances as model_travel_allowances
from schema import Travel_allowances as schema_travel_allowances
from config import get_db
from sqlalchemy.orm import Session

router = APIRouter()
""" Post data """
""" Travel Allowances """


@router.post('/post_travel_allowances',
             response_model=schema_travel_allowances)
async def post_travel_allowances(
        travel_allowances_add: schema_travel_allowances):

    try:
        amount_of_days = (travel_allowances_add.end_date -
                          travel_allowances_add.start_date).days + 1
        travel_allowances_amount = travel_allowances_add.travel_allowances
        travel_allowances_amount_total = amount_of_days * travel_allowances_amount

        db_travel_allowances = model_travel_allowances(
            name=travel_allowances_add.name.lower().split(),
            amount_of_days=amount_of_days,
            start_date=travel_allowances_add.start_date,
            end_date=travel_allowances_add.end_date,
            travel_allowances=travel_allowances_amount_total)

        db.session.add(db_travel_allowances)
        db.session.commit()

        return db_travel_allowances

    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Get Data """


@router.get('/get_travel_allowances')
async def get_traverl_allowances(name: str = Query(None,
                                                   description='Driver Name'),
                                 limit: int = Query(None,
                                                    description='Limit',
                                                    le=100),
                                 db: Session = Depends(get_db)):

    query = db.query(model_travel_allowances.name,
                     model_travel_allowances.amount_of_days,
                     model_travel_allowances.travel_allowances,
                     model_travel_allowances.start_date,
                     model_travel_allowances.end_date)

    try:
        if name:
            query = query.filter(model_travel_allowances.name == name.lower().split())

        query = query.limit(limit)

        travel_allowances_data = query.all()

        travel_allowances_data_dicts = [
            dict((key, value.lower() if isinstance(value, str) else value)
                 for key, value in row._asdict().items())
            for row in travel_allowances_data
        ]

        return travel_allowances_data_dicts

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Delete data """

@router.delete('/delete_travel_allowances')
async def delete_travel_allowances(
    name: str = Query(None, description='Driver name',
                      alias='driver_name'),
    start_date: str = Query(None, description='Start Date'),
    end_date: str = Query(None, description='End Date'),
    db: Session = Depends(get_db)):
    # сделать проверку (всплывающее окно например или что-то подобное)
    # если мы удаляем только по имени водителя
    # или лучше сделать start_date и end_start обязательными полями
    try:
        travel_allowances_query = db.query(model_travel_allowances).filter(
            model_travel_allowances.name == name.lower().split(),
            model_travel_allowances.start_date == start_date.lower().split(),
            model_travel_allowances.end_date == end_date.lower().split()).all()

        if not travel_allowances_query:
            raise HTTPException(status_code=404,
                                detail='Travel allowances data not found')

        for travel_allowances in travel_allowances_query:
            db.delete(travel_allowances)

        db.commit()

        return {'message': 'Travel allowances data deleted succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Patch Data """
# подумать как можно улучшить выборку данных

@router.patch('/update_travel_allowances')
async def update_travel_allowances(
        name: str = Query(None, description='Driver Name',
                        alias='driver_name'),
        start_date: str = Query(None, description='Start date'),
        end_date: str = Query(None, description='End date'),
        new_start_date: str = Query(None, description='Set new start date'),
        new_end_date: str = Query(None, description='Set new end date'),
        new_travel_allowances: str = Query(None, description='Set new travel allowances'),
        db: Session = Depends(get_db)):
    try:
        travel_allowances_query = db.query(model_travel_allowances).filter(
            model_travel_allowances.name == name.lower().split(),
            model_travel_allowances.start_date == start_date.lower().split(),
            model_travel_allowances.end_date == end_date.lower().split()).first()

        if not travel_allowances_query:
            raise HTTPException(status_code=404,
                                detail = 'Driver travel allowances not found')

        if new_start_date is not None:
            travel_allowances_query.start_date = new_start_date

        if new_end_date is not None:
            travel_allowances_query.end_date = new_end_date

        if new_travel_allowances is not None:
            travel_allowances_query.travel_allowances = new_travel_allowances

        db.commit()

        return {'message': 'Data updated successfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')
