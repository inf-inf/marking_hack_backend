from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from dependencies.sql_db import get_db


router_retail = APIRouter(
    prefix='/retail',
    tags=['retail']
)


def get_loss_rate(percent: float, light: bool = False) -> str:
    """ Цвета для обозначения уровня потерь на карте """
    if percent < -10:
        return '#93ffac' * light or '#28a745'   # Зеленый
    elif -10 <= percent <= 0:
        return '#ffff9b' * light or '#ffc107'   # Желтый
    return '#fc7462' * light or '#dc3545'       # Красный


@router_retail.get('/get_stores', summary='Получить торговые точки')
def get_stores(inn: str = '6B8E111AB5B5C556C0AEA292ACA4D88B',
               page: int = 1,
               limit: int = 10,
               db: Session = Depends(get_db)):

    skip = limit * page - limit
    sql = """
        SELECT
            s.id_sp,
            s.region_code,
            s.city_with_type,
            s.city_fias_id,
            s.postal_code,
            SUM(
                    (
                        (current_date - rp.last_update_date) * rp.avg_cnt_per_day - rp.cnt
                    ) * rp.price / rp.avg_month * 100
                )  as loss_percentage
        FROM public.stores AS s
        JOIN public.retail_points AS rp ON s.id_sp = rp.id_sp
        WHERE rp.avg_month > 0 AND s.inn = :inn
        GROUP BY s.id_sp, s.region_code, s.city_with_type, s.city_fias_id, s.postal_code
        ORDER BY loss_percentage DESC
        LIMIT :limit
        OFFSET :skip
    """
    params = {
        'inn': inn,
        'skip': skip,
        'limit': limit
    }
    stores = db.execute(text(sql), params).all()

    sql = """
        SELECT COUNT(*) AS stores_total
        FROM
        (
            SELECT COUNT(*)
            FROM public.stores AS s
            JOIN public.retail_points AS rp ON s.id_sp = rp.id_sp
            WHERE rp.avg_month > 0 AND s.inn = :inn
            GROUP BY rp.id_sp
        ) AS s
        """
    stores_total = db.execute(text(sql), {'inn': inn}).first().stores_total
    from random import randint
    res = {
        'stores': [
            {
                'id_sp': s.id_sp,
                'region_code': s.region_code,
                'city_with_type': s.city_with_type,
                'city_fias_id': str(s.city_fias_id),
                'postal_code': s.postal_code,
                'name': 'Название точки',
                'geo_lat': 55 + randint(450000, 780000) / 1000000,  # Временно рандомные координаты
                'geo_lon': 37 + randint(450000, 780000) / 1000000,  # пока в базе нет реальных
                'loss_percentage': float(s.loss_percentage),
                'loss_rate_dark': get_loss_rate(float(s.loss_percentage)),
                'loss_rate_light': get_loss_rate(float(s.loss_percentage), light=True)
            } for s in stores
        ],
        'stores_total': stores_total
    }

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
