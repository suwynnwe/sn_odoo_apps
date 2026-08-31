import re
from bs4 import BeautifulSoup
from odoo import models
from ..util.myanmar_reshaper import reshape_myanmar_word


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _prepare_html(self, html, report_model=False):
        is_bytes = isinstance(html, bytes)
        html_string = html.decode("utf-8") if is_bytes else html

        soup = BeautifulSoup(html_string, "html.parser")
        myanmar_regex = re.compile(r"[\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF]+")

        def reshape_myanmar_only(match):
            return reshape_myanmar_word(match.group(0))

        for text_node in soup.find_all(string=True):
            if text_node.parent and text_node.parent.name in ["script", "style"]:
                continue

            if myanmar_regex.search(text_node):
                new_text = myanmar_regex.sub(reshape_myanmar_only, text_node)
                text_node.replace_with(new_text)

        reshaped_html = str(soup)
        prepared_html = reshaped_html.encode("utf-8") if is_bytes else reshaped_html
        return super()._prepare_html(prepared_html, report_model)
