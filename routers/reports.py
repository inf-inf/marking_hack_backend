from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session

from models.files.images import get_file_preview
from models.files.pdf_generator import PDFGenerator
from dependencies.sql_db import get_db
from sql_db.orm_models.reports import Report

router_reports = APIRouter(
    prefix='/reports',
    tags=['reports']
)


class PDFResponse(Response):
    media_type = 'application/pdf'


@router_reports.post('/save', summary='Сохранение данных по отчету')
def save(db: Session = Depends(get_db)):
    """ Сохранить данные пользователя. Возвращает PDF """

    pdf_gen = PDFGenerator('report.html')
    pdf_file = pdf_gen.get_file

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    d = {   # мок пока параметры с фронта не приходят
        'dt_created': dt_str,
    }
    db_report = Report(
        type=1,
        name=file_name,
        data=d
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

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


@router_reports.get('/v2/get_pdf', summary='Получение файла отчета в формате PDF')
def get_pdf(report_id: int, db: Session = Depends(get_db)):
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


@router_reports.get('/get_list', summary='Список отчетов')
def get_list(db: Session = Depends(get_db)):
    """ Возвращает список доступных id отчетов для метода `/reports/v2/get_pdf` """

    res = [
        {
            'id': 1,
            'name': 'name1.pdf',
            'preview': get_file_preview()
        },
        {
            'id': 2,
            'name': 'name2.pdf',
            'preview': get_file_preview()
        }
    ]

    return JSONResponse(res)
