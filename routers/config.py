from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from dependencies.sql_db import get_db
from schemas.config import SetConfig


router_config = APIRouter(
    prefix='/config',
    tags=['config']
)


@router_config.post('/set', summary="Конфигурирование цветов отображения уведомлений")
def config(conf: SetConfig, db: Session = Depends(get_db)):
    sql = """
        UPDATE public.config
        SET good_percent_limit = :good_percent_limit, warn_percent_limit = :warn_percent_limit
    """
    params = {
        'good_percent_limit': conf.good_percent_limit,
        'warn_percent_limit': conf.warn_percent_limit
    }
    db.execute(text(sql), params)
    return params
