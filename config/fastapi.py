""" Конфигурация фреймворка FastAPI """

FASTAPI_KWARGS = {
    'title': 'Marking Hack API',
    'description': 'Хакатон по созданию системы управления товарами на основе данных «Честного знака»',
    'docs_url': '/admin/docs',
    'redoc_url': None,
    'openapi_url': '/admin/openapi.json',
}

CORS_KWARGS = {
    'allow_origins': ["*"],
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"],
}