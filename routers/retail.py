from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from dependencies.sql_db import get_db


router_retail = APIRouter(
    prefix='/retail',
    tags=['retail']
)


def get_loss_rate(percent: float) -> str:
    """ Цвета для обозначения уровня потерь на карте """
    if percent < 0:
        return '#28a745'
    elif 0 <= percent < 3:
        return '#ffc107'
    return '#dc3545'


@router_retail.get('/get_stores', summary='Получить торговые точки')
def get_stores(inn: str = '', db: Session = Depends(get_db)):

    res = [
        {
            'id_sp': 'A44F290366CE1023507C993710313E3E',
            'name': 'Такая себе точка',
            'geo_lat': 55.787133,
            'geo_lon': 37.686877,
            'loss_percentage': 5,
            'loss_rate': get_loss_rate(5)
        },
        {
            'id_sp': 'D4079C72BE0EE138A787385DD327DF2E',
            'name': 'Отличная точка',
            'geo_lat': 55.741292,
            'geo_lon': 37.415792,
            'loss_percentage': -10,
            'loss_rate': get_loss_rate(-10)
        },
        {
            'id_sp': '95E5F1CB2478D04148F32E04509712B8',
            'name': 'Быдло точка',
            'geo_lat': 55.590990,
            'geo_lon': 37.647963,
            'loss_percentage': 11,
            'loss_rate': get_loss_rate(11)
        },
        {
            'id_sp': '44EF61711FD55ACC27AC2A767C655355',
            'name': 'Вполне себе точка',
            'geo_lat': 55.900998,
            'geo_lon': 37.742439,
            'loss_percentage': 0.5,
            'loss_rate': get_loss_rate(0)
        },
    ]
    return JSONResponse(res)


@router_retail.get('/get_store_gtins', summary='Получить GTINы торговой точки')
def get_store_gtins(id_sp: str, db: Session = Depends(get_db)):

    res = [
        {
            'gtin': '6AB0A3B1D3D427F951C7BDE5C59FE8A0',
            'product_name': 'молоко',
            'product_short_name': 'млк',
            'tnved': 'че это',
            'tnved10': 'лан',
            'brand': 'inf-inf',
            'loss_percentage': -10,
            'loss_rate': get_loss_rate(-15),
            'message': 'Товара хватит на 15 дней',
        },
        {
            'gtin': '6AB0A3B1D3D427F951C7BDE5C59FE8A1',
            'product_name': 'биткоин',
            'product_short_name': 'btc',
            'tnved': 'че это',
            'tnved10': 'лан',
            'brand': 'бинанс',
            'loss_percentage': 5,
            'loss_rate': get_loss_rate(5),
            'message': 'Товара хватит на 1 день',
        },
        {
            'gtin': '6AB0A3B1D3D427F951C7BDE5C59FE8A2',
            'product_name': 'холодильник',
            'product_short_name': 'шкаф',
            'tnved': 'че это',
            'tnved10': 'лан',
            'brand': 'диван',
            'loss_percentage': 0.3,
            'loss_rate': get_loss_rate(0.3),
            'message': 'Товара хватит на 4 дня',
        },

    ] * 100
    return JSONResponse(res)
