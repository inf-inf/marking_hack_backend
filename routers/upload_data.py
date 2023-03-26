from fastapi import APIRouter, Depends, File, UploadFile
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.upload_data import RetailOut

from dependencies.sql_db import get_db


router_upload = APIRouter(
    prefix='/upload',
    tags=['upload']
)


@router_upload.post('/csv', summary='Загрузить csv файл с новыми данными')
def save_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_name = f'data_{datetime.now()}.csv'
    # new_csv = open(f'../files/{file_name}', mode='w')
    # new_csv.write(file.read())
    # new_csv.close()
    return {'file_name': file_name}


@router_upload.post('/data')
def save_data_like_csv(data: RetailOut):
    file_name = f'data_{datetime.now()}.json'
    # new_csv = open(f'../files/{file_name}', mode='w')
    # new_csv.write(data.json(exclude_unset=True))
    # new_csv.close()
    return {'file_name': file_name}
