from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi_sqlalchemy import db
from schema import Driver_penalty as schema_driver_penalty
from models import Driver_penalty as model_driver_penalty
from config import get_db
from sqlalchemy.orm import Session

router = APIRouter()
""" Post data """


@router.post('/post_penalty', response_model=schema_driver_penalty)
async def post_penalty(penalty_add: schema_driver_penalty):
    try:
        db_post_penalty = model_driver_penalty(
            name=penalty_add.name.lower(),
            penalty_amount=penalty_add.penalty_amount,
            penalty_cause=penalty_add.penalty_cause.lower(),
            penalty_date=penalty_add.penalty_date)

        db.session.add(db_post_penalty)
        db.session.commit()

        return db_post_penalty

    except HTTPException as e:
        return e
    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Get Data """

# сделать, чтобы штрафы высчитывались автоматически
# из зарплаты за определенный период (месяц)


@router.get('/get_driver_penalty')
async def get_driver_penalty_from_db(
        name: str = Query(None, description='Driver Name'),
        penalty_date: str = Query(None, description='Penalty Date'),
        limit: int = Query(None, description='Limit', le=100),
        db: Session = Depends(get_db)):
    try:
        query = db.query(model_driver_penalty.name,
                         model_driver_penalty.penalty_amount,
                         model_driver_penalty.penalty_cause,
                         model_driver_penalty.penalty_date)
        if name:
            query = query.filter(model_driver_penalty.name == name.lower().split())

        if penalty_date:
            query = query.filter(
                model_driver_penalty.penalty_date == penalty_date)

        query = query.limit(limit)

        penalty_data = query.all()

        if penalty_data is None:
            raise HTTPException(status_code=404,
                                detail='Driver penalty data not found')

        penalty_data_dicts = [
            dict((key, value.lower() if isinstance(value, str) else value)
                 for key, value in row._asdict().items())
            for row in penalty_data
        ]

        return penalty_data_dicts

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Delete Data """

@router.delete('/delete_driver_penalty')
async def delete_driver_penalty(
        name: str = Query(None, description='Driver Name',
                          alias='driver_name'),
        # alias используется для альтернативного имени в параметре запроса
        penalty_date: str = Query(None, description='Penalty Date'),
        db: Session = Depends(get_db)):
    try:
        penalty_query = db.query(model_driver_penalty).filter(
            model_driver_penalty.name == name.lower().split(),
            model_driver_penalty.penalty_date == penalty_date.split()).all()

        if not penalty_query:
            raise HTTPException(status_code=404,
                                detail='Driver penalty data not found')

        for penalty in penalty_query:
            db.delete(penalty)

        db.commit()

        return {'message': 'Penalty data deleted succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Patch Data """

@router.patch('/update_driver_penalty')
async def update_driver_penalty(
        name: str = Query(None, description='Driver Name',
                          alias='driver_name'),
        penalty_date: str = Query(None, description='Penalty Date'),
        new_penalty_amount: int = Query(None, description='New Penalty Amount'),
        new_penalty_cause: str = Query(None, description='New Penalty Cause'),
        db: Session = Depends(get_db)):
    try:
        penalty_query = db.query(model_driver_penalty).filter(
            model_driver_penalty.name == name.lower().split(),
            model_driver_penalty.penalty_date == penalty_date.split()).first()

        if not penalty_query:
            raise HTTPException(status_code=404,
                                detail='Driver penalty data not found')

        if new_penalty_amount is not None:
            penalty_query.penalty_amount = new_penalty_amount
        if new_penalty_cause is not None:
            penalty_query.penalty_cause = new_penalty_cause

        db.commit()

        return {'message': 'Penalty data updated successfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')



# добавить возможность удаление данных и/или их замену!!!!
# почитать про restful api
# сделать регистрацию пользователей с различными уровнями доступа
