from fastapi import APIRouter, Depends, File, UploadFile
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.upload_data import RetailOut

from dependencies.sql_db import get_db


router_config = APIRouter(
    prefix='/config',
    tags=['config']
)


@router_config.post('/set', summary="Конфигурирование цветов отображения уведомлений")
def config(good_percent_limit: float, warn_percent_limit: float, db: Session = Depends(get_db)):
    db.execute(text('UPDATE public.config '
                    'SET good_percent_limit = :good_percent_limit, '
                    '    warn_percent_limit = :warn_percent_limit'))
    return {'good_percent_limit': good_percent_limit, 'warn_percent_limit': warn_percent_limit}
