import pdfkit

from models.files.html_generator import HTMLGenerator
from config.files import WKHTMLTOPDF_PATH


class PDFGenerator:
    """ Создание PDF на основе HTML шаблона """

    _pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    def __init__(self, template_file: str, **kwargs):
        """
        :param template_file: Имя файла относительно папки с шаблонами, например, "report.html"
        :param kwargs: Параметры, передаваемые в шаблон
        """
        self._html_generator = HTMLGenerator(template_file)
        source_html = self._html_generator.render(**kwargs)

        self._pdf_bytes = pdfkit.from_string(source_html, configuration=self._pdfkit_config)

    @property
    def get_file(self) -> bytes:
        """ Получить PDF файл bytes """
        return self._pdf_bytes

    def save_file(self, file_path: str):
        """
        Сохранить PDF файл на диск

        :param file_path: Имя файла (включая путь) с которым будет сохранен PDF документ
        """
        with open(file_path, 'wb') as new_file:
            new_file.write(self._pdf_bytes)
