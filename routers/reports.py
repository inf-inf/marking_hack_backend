from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from models.files.pdf_generator import PDFGenerator

router_reports = APIRouter(
    prefix='/reports',
    tags=['reports']
)


class PDFResponse(Response):
    media_type = 'application/pdf'


@router_reports.post('/save', summary='Сохранение данных по отчету', response_class=PDFResponse)
def save():
    """ Сохранить данные пользователя. Возвращает PDF """

    pdf_gen = PDFGenerator('report.html')
    pdf_file = pdf_gen.get_file

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    res = {
        "success": True,
        "filename": file_name,
        "file": list(pdf_file)
    }

    return JSONResponse(res)


@router_reports.get('/get_pdf',
                    summary='Получение файла отчета в формате PDF',
                    response_class=PDFResponse,
                    deprecated=True
                    )
def get_pdf():
    """ Возвращает файл PDF bytes"""

    pdf_gen = PDFGenerator('report.html')
    pdf_file = pdf_gen.get_file

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
    return PDFResponse(pdf_file, headers=headers)


@router_reports.get('/v2/get_pdf', summary='Получение файла отчета в формате PDF', response_class=PDFResponse)
def get_pdf(report_id: int):
    """ Возвращает файл PDF json bytes array"""

    pdf_gen = PDFGenerator('report.html')
    pdf_file = pdf_gen.get_file

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    res = {
        "success": True,
        "filename": file_name,
        "file": list(pdf_file)
    }

    return JSONResponse(res)


@router_reports.get('/get_list', summary='Список отчетов', response_class=PDFResponse)
def get_list():
    """ Возвращает список доступных id отчетов для метода `/reports/v2/get_pdf` """

    res = {
        "success": True,
        "reports": [1, 2, 3, 4, 5],
    }

    return JSONResponse(res)
