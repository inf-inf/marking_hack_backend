from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from dependencies.sql_db import get_db
from models.retail.stores import get_loss_rate, get_days_overdue_msg


router_retail = APIRouter(
    prefix='/retail',
    tags=['retail']
)


@router_retail.get('/get_stores', summary='Получить торговые точки')
def get_stores(inn: str = '6B8E111AB5B5C556C0AEA292ACA4D88B',
               page: int = 1,
               limit: int = 30,
               db: Session = Depends(get_db)):

    skip = limit * page - limit
    sql = """
        SELECT
            s.id_sp,
            s.region_code,
            s.city_with_type,
            s.city_fias_id,
            s.postal_code,
            ROUND(SUM(
                    (
                        (current_date - rp.last_update_date) * rp.avg_cnt_per_day - rp.cnt
                    ) * rp.price / rp.avg_month * 100
                ), 2)  as loss_percentage
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
def get_store_gtins(id_sp: str,
                    page: int = 1,
                    limit: int = 15,
                    db: Session = Depends(get_db)):
    skip = limit * page - limit
    sql = """
        SELECT
            rp.gtin,
            products.product_name,
            products.product_short_name,
            products.tnved,
            products.tnved10,
            products.brand,
            products.country,
            ROUND(((
                (current_date - rp.last_update_date) * rp.avg_cnt_per_day - rp.cnt
            ) * rp.price / rp.avg_month * 100), 2)  as loss_percentage,
            (
                ((current_date - rp.last_update_date) * rp.avg_cnt_per_day - rp.cnt) / rp.avg_cnt_per_day
            )::integer AS days_overdue
        FROM public.retail_points AS rp
        JOIN public.products AS products ON products.gtin = rp.gtin
        WHERE rp.avg_month > 0 AND rp.id_sp = :id_sp 
        ORDER BY loss_percentage DESC
        LIMIT :limit
        OFFSET :skip
        """
    params = {
        'id_sp': id_sp,
        'skip': skip,
        'limit': limit
    }
    gtins = db.execute(text(sql), params).all()

    sql = """
        SELECT COUNT(*) AS gtins_total
        FROM public.retail_points AS rp
        JOIN public.products AS products ON products.gtin = rp.gtin
        WHERE rp.avg_month > 0 AND rp.id_sp = :id_sp
            """
    gtins_total = db.execute(text(sql), {'id_sp': id_sp}).first().gtins_total

    res = {
        'gtins': [
            {
                'gtin': g.gtin,
                'product_name': g.product_name,
                'product_short_name': g.product_short_name,
                'tnved': g.tnved,
                'tnved10': g.tnved10,
                'brand': g.brand,
                'country': g.country,
                'loss_percentage': float(g.loss_percentage),
                'loss_rate_dark': get_loss_rate(float(g.loss_percentage)),
                'loss_rate_light': get_loss_rate(float(g.loss_percentage), light=True),
                'message': get_days_overdue_msg(g.days_overdue)
            } for g in gtins
        ],
        'gtins_total': gtins_total
    }

    return JSONResponse(res)
