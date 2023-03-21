from fastapi import APIRouter, responses

router_common = APIRouter(
    tags=['common']
)


@router_common.get('/ping', summary='Проверка доступности API')
def ping():
    """
    Метод должен возвращать 'pong' в body
    """
    return responses.PlainTextResponse('pong')
