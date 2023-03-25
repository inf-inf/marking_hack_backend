import base64
from pathlib import Path

from config.files import STATIC_PATH


def get_file_preview():
    """ Получить изображение для превью файла """
    logo_path = Path(STATIC_PATH, 'img', 'pdf_logo.png')
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    return encoded_string
