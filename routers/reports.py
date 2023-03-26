from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session

from models.files.images import get_file_preview
from models.files.pdf_generator import PDFGenerator
from dependencies.sql_db import get_db
from sql_db.orm_models.reports import Report
from schemas.reports import NewReport

router_reports = APIRouter(
    prefix='/reports',
    tags=['reports']
)


class PDFResponse(Response):
    media_type = 'application/pdf'


@router_reports.post('/save', summary='Сохранение данных по отчету')
def save(report_data: NewReport, db: Session = Depends(get_db)):
    """ Сохранить данные пользователя. Возвращает PDF """

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    d = {
        'dt_created': dt_str,
        'report_data': report_data.dict(),
    }

    pdf_gen = PDFGenerator('report.html', **d)
    pdf_file = pdf_gen.get_file

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

    pdf_data = db.query(Report).filter(Report.id == report_id).first()

    pdf_gen = PDFGenerator('report.html', **pdf_data.data)
    pdf_file = pdf_gen.get_file

    res = {
        "success": True,
        "filename": pdf_data.name,
        "file": list(pdf_file)
    }

    return JSONResponse(res)


@router_reports.get('/get_list', summary='Список отчетов')
def get_list(page: int = 1, limit: int = 18, db: Session = Depends(get_db)):
    """ Возвращает список доступных id отчетов для метода `/reports/v2/get_pdf` """

    skip = limit * page - limit
    reports_db = db.query(Report).order_by(Report.id.desc()).offset(skip).limit(limit).all()
    reports_total = db.query(Report).count()
    preview = get_file_preview()

    res = {
        'reports': [
            {
                'id': report.id,
                'name': report.name,
                'preview': preview
            } for report in reports_db
        ],
        'total': reports_total
    }

    return JSONResponse(res)
