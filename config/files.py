import os
from pathlib import Path

CURRENT_PATH = Path(__file__).absolute().parent.parent
HTML_TEMPLATES_PATH = Path(CURRENT_PATH, 'templates')
WKHTMLTOPDF_PATH = os.environ.get('WKHTMLTOPDF_PATH', '')
