from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import Response
from models.files.pdf_generator import PDFGenerator

router_files = APIRouter(
    prefix='/files',
    tags=['files']
)


class PDFResponse(Response):
    media_type = 'application/pdf'


@router_files.post('/create_pdf', summary='Создание отчета в формате PDF', response_class=PDFResponse)
def create_pdf():
    """ Возвращает файл PDF """

    pdf_gen = PDFGenerator('report.html')
    pdf_file = pdf_gen.get_file

    dt_str = datetime.now().strftime('%d.%m.%Y %H-%M-%S')
    file_name = f'report_{dt_str}.pdf'

    headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
    return PDFResponse(pdf_file, headers=headers)
