import uvicorn
from fastapi import FastAPI
from config import DATABASE_URL
from fastapi_sqlalchemy import DBSessionMiddleware
from routers import add_driver_data_router
from routers import add_new_car_router
from routers import post_salary_router
from routers import post_penalty_router
from routers import post_travel_allowances_router
from routers import add_scan_documents_router

app = FastAPI(title='GrandoSchedule')

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

# imported routers
app.include_router(add_driver_data_router.router)
app.include_router(add_new_car_router.router)
app.include_router(post_salary_router.router)
app.include_router(post_penalty_router.router)
app.include_router(post_travel_allowances_router.router)
app.include_router(add_scan_documents_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# new update - uwu
