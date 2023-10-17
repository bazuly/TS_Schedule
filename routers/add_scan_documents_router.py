from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi_sqlalchemy import db
from schema import Document_create, Document_response
from models import Document_data as model_document_data
from sqlalchemy.orm import Session
from config import get_db

router = APIRouter()
""" Post pdf, jpg e.t.c """


@router.post("/upload_document/")
async def upload_document(title: str, file: UploadFile = File(...)):
    try:

        file_data = file.file.read()

        document = model_document_data(title=title, file_data=file_data)
        db.session.add(document)
        db.session.commit()

        return {"id": document.id, "title": document.title}

    except HTTPException as e:
        return print(e)
    except Exception:
        return HTTPException(status_code=500, detail="Internal Server Error")


""" DELETE DATA """


@router.delete('/delete_scan_document')
async def delete_scan_document(
        # подразумевается, что мы будем выбирать данные по title.
        # title == имя водителя, по нему и будем ориентироваться
        # можно еще по id, но это такое
        title: str = Query(None, description='Document title'),
        db: Session = Depends(get_db)):
    try:
        document_query = db.query(model_document_data).filter(
            model_document_data.title == title.lower().strip().split())

        if not document_query:
            raise HTTPException(status_code=404,
                                detail='Document scan data not found')

        for doc in document_query:
            db.delete(doc)

        db.commit()

        return {'message': 'Data deleted succesfully'}

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


""" Get document """

# заработало, но я не до конца понял, скорее всего оно не возвращает картинку
# нужно еще чтобы возвращало картинку, как, пока хз 
# надо это реализовать через url, который будет лежать в базе данных
@router.get("/get_driver_dcument")
async def get_scan_document(title: str = Query(...)):
    try:
        document = db.session.query(model_document_data).filter(
            model_document_data.title == title).first()

        if not document:
            raise HTTPException(status_code=404,
                                detail='Document data not found')

        return Document_response(id=document.id, title=document.title)

    except HTTPException as e:
        return e

    except Exception as e:
        return HTTPException(status_code=500, detail='Internal Server Error')


# возможно стоит добавить возможность загружать скан заявки