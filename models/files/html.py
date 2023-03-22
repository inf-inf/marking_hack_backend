from jinja2 import Environment, FileSystemLoader

from config.files import HTML_TEMPLATES_PATH


class HTMLRenderer:
    """ Рендеринг HTML по шаблонам через jinja2 """

    _template_env = Environment(loader=FileSystemLoader(HTML_TEMPLATES_PATH))

    def __init__(self, template_file: str):
        """
        :param template_file: Имя файла относительно папки с шаблонами, например, "report.html"
        """
        self._template = self._template_env.get_template(template_file)

    def render(self, **kwargs) -> str:
        """
        Рендеринг HTML

        :param kwargs: Параметры, передаваемые в шаблон
        :return:
        """
        output_text = self._template.render(**kwargs)
        return output_text
