from fastapi import APIRouter, HTTPException, Depends, Query
from models import Driver_salary as model_driver_salary
from schema import Driver_salary as schema_driver_salary
from fastapi_sqlalchemy import db
from config import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()
""" Post data """
""" Salary """

# Добавление зарпалты за определенный период
# Например за рейс, который длился три дня
# В теории можно добавить еще комментарий


@router.post('/post_salary', response_model=schema_driver_salary)
async def post_salary(salary_add: schema_driver_salary):
    try:
        db_post_salary = model_driver_salary(
            name=salary_add.name.lower().split(),
            salary_amount=salary_add.salary_amount,
            start_date=salary_add.start_date,
            end_date=salary_add.end_date)

        db.session.add(db_post_salary)
        db.session.commit()

        return db_post_salary

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


# В данном эндопоинте можно узнать зарплату конкретного водителя
# За определенный период

# Добавить возможнсть получение ЗП за определенный период
# С учетом вычита штрафов (хотя нам это в в рамках этого проекта нахуй не уперлось)
""" Get data """


@router.get('/get_driver_salary')
async def get_driver_salary_from_db(
        name: str = Query(None, description='Driver Salary'),
        start_date: str = Query(None, description='Start Date'),
        end_date: str = Query(None, description='End Date'),
        db: Session = Depends(get_db)):

    try:
        query = db.query(model_driver_salary.name,
                         model_driver_salary.salary_amount,
                         model_driver_salary.start_date,
                         model_driver_salary.end_date)

        if name:
            query = query.filter(model_driver_salary.name == name.lower().split())

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(model_driver_salary.start_date >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(model_driver_salary.end_date <= end_date)

        driver_salary_data = query.all()

        total_salary = 0

        result = []

        for row in driver_salary_data:
            data = row._asdict()
            data['name'] = data['name'].lower()
            result.append(data)

            if start_date and end_date:
                if row.start_date >= start_date and row.end_date <= end_date:
                    total_salary += row.salary_amount

        if total_salary > 0:
            result.append({'total_salary': total_salary})

        return result

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')
    
    
""" Delete Data """

@router.delete('/delete_salary')
async def delete_driver_salary(
    name: str = Query(None, description='Driver Name',
                      alias='driver_name'),
    start_date: str = Query(None, description='Start date'),
    end_date: str = Query(None, description='End date'),
    db: Session = Depends(get_db)):
    
    try:
        driver_salary_query = db.query(model_driver_salary).filter(
            model_driver_salary.name == name.lower().split(),
            model_driver_salary.start_date == start_date.lower().split(),
            model_driver_salary.end_date == end_date.lower().split()).all()
        
        if not driver_salary_query:
            raise HTTPException(status_code=404,
                                detail='Driver salary not found')
        
        for driver_salary in driver_salary_query:
            db.delete(driver_salary)
        
        db.commit()
        
        return {'message': 'Driver salary data deleted succesfully'}
    
    except HTTPException as e:
        return e
    
    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')

    
""" Patch data """

@router.patch('/update_driver_salary')
async def update_driver_salary(
        name: str = Query(None, description='Driver Name',
                        alias='driver_name'),
        start_date: str = Query(None, description='Start date'),
        end_date: str = Query(None, description='End date'),
        new_start_date: str = Query(None, description='Set new start date'),
        new_end_date: str = Query(None, description='Set new end date'),
        new_driver_salary: str = Query(None, description='Set new travel allowances'),
        db: Session = Depends(get_db)):
    try:
        travel_allowances_query = db.query(model_driver_salary).filter(
            model_driver_salary.name == name.lower(),
            model_driver_salary.start_date == start_date.lower().split(),
            model_driver_salary.end_date == end_date.lower().split()).first()

        if not travel_allowances_query:
            raise HTTPException(status_code=404,
                                detail = 'Driver travel allowances not found')

        if new_start_date is not None:
            travel_allowances_query.start_date = new_start_date

        if new_end_date is not None:
            travel_allowances_query.end_date = new_end_date

        if new_driver_salary is not None:
            travel_allowances_query.travel_allowances = new_driver_salary

        db.commit()

        return {'message': 'Data updated successfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')