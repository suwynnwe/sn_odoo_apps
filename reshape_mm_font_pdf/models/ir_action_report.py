from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _prepare_html(self, html, report_model=False):
        html_string = html.decode('utf-8')
        new_word = reshape_myanmar_font(html_string)
        html = new_word.encode('utf-8')
        return super()._prepare_html(html, report_model)


def reshape_myanmar_font(html):
    html_list = list(html)

    # Step - 1: Reorder the characters
    ###########
    # Reorder the 'ThaWaiHtoo' character
    for i, v in enumerate(html_list):
        if v == '\u1031':
            if html_list[i - 1] in ['\u103B', '\u103C', '\u103D', '\u103E']:
                html_list[i - 1], html_list[i] = html_list[i], html_list[i - 1]
                if html_list[i - 2] in ['\u103B', '\u103C', '\u103D', '\u103E']:
                    html_list[i - 2], html_list[i - 1] = html_list[i - 1], html_list[i - 2]
                    if html_list[i - 3] in ['\u103B', '\u103C', '\u103D', '\u103E']:
                        html_list[i - 3], html_list[i - 2] = html_list[i - 2], html_list[i - 3]

    # Reorder the 'YaYit' character
    for i, v in enumerate(html_list):
        if v == '\u103C':
            if html_list[i - 1] == '\u1031':
                html_list[i - 2], html_list[i - 1], html_list[i] = '\u001D\u1031', html_list[i], html_list[i - 2]
            else:
                html_list[i - 1], html_list[i] = html_list[i], html_list[i - 1]

    # Step 2: Substitute the characters
    #########
    # 'YaYit' character substitutions
    for i, v in enumerate(html_list):
        if v == '\u103C':
            if html_list[i + 1] in ['\u1000', '\u1003', '\u100F', '\u1006', '\u1010', '\u1011',
                                    '\u1018', '\u101A', '\u101C', '\u101E', '\u101F', '\u1021']:
                html_list[i] = '\uE1B2'

    # One-to-One character substitutions
    for i, v in enumerate(html_list):
        if v == '\u1014':
            if html_list[i + 1] in ['\u102F', '\u1030', '\u103D', '\u103E']:
                html_list[i] = '\uE107'
            if html_list[i + 2] in ['\u102F', '\u1030']:
                html_list[i] = '\uE107'
            if html_list[i + 1] == '\u1031':
                if html_list[i + 2] in ['\u102F', '\u1030', '\u103D', '\u103E']:
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\u001D\u1031', '\uE107', html_list[i + 2]
        if v == '\u101B':
            if html_list[i + 1] in ['\u102F', '\u1030']: html_list[i] = '\uE108'
            if html_list[i + 2] in ['\u102F', '\u1030']: html_list[i] = '\uE108'
            if html_list[i + 3] in ['\u102F', '\u1030']: html_list[i] = '\uE108'
        if v == '\u102F':
            if html_list[i - 1] == '\u103B' or html_list[i - 2] == '\u103B':
                html_list[i] = '\uE2F1'
            if html_list[i - 2] in ['\u103C', '\uE1B2'] or html_list[i - 3] in ['\u103C', '\uE1B2']:
                html_list[i] = '\uE2F1'
        if v == '\u1030':
            if html_list[i - 1] == '\u103B' or html_list[i - 2] == '\u103B':
                html_list[i] = '\uE2F2'
            if html_list[i - 2] in ['\u103C', '\uE1B2'] or html_list[i - 3] in ['\u103C', '\uE1B2']:
                html_list[i] = '\uE2F2'
        if v == '\u1037':
            if html_list[i - 1] in ['\u102F', '\u1030']:
                html_list[i] = '\uE037'
            if html_list[i - 1] == '\u1014' or html_list[i - 2] == '\u1014':
                html_list[i] = '\uE037'
            if html_list[i - 1] in ['\uE2F1', '\uE2F2', '\u103D']:
                html_list[i] = '\uE137'
            if html_list[i - 1] == '\u103B' or html_list[i - 2] == '\u103B':
                html_list[i] = '\uE137'
            if html_list[i - 1] == '\u103E' or html_list[i - 2] == '\u103E':
                if html_list[i - 3] == '\u101B':
                    html_list[i] = '\uE137'
                else:
                    html_list[i] = '\uE037'
        if v == '\u103E':
            if html_list[i - 2] in ['\u103C', '\uE1B2']:
                html_list[i] = '\uE1F3'

    # Two-to-One character substitutions
    for i, v in enumerate(html_list):
        if v == '\u102D':
            if html_list[i + 1] == '\u1036':
                html_list[i], html_list[i + 1] = '\uE2D1', ''
            if html_list[i + 1] == '\u1032':
                html_list[i], html_list[i + 1] = '\uE12D', ''
        if v == '\u102B':
            if html_list[i + 1] == '\u103A':
                html_list[i], html_list[i + 1] = '\uE02D', ''
            if html_list[i + 1] == '\u1032':
                html_list[i], html_list[i + 1] = '\uE52C', ''
            if html_list[i + 1] == '\u1036':
                html_list[i], html_list[i + 1] = '\uE52B', ''
        if v == '\u103B':
            if html_list[i + 1] == '\u103D':
                html_list[i], html_list[i + 1] = '\uE1A4', ''
                if html_list[i + 2] == '\u103E':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE1D1', '\u103B', ''
            if html_list[i + 1] == '\u103E':
                html_list[i], html_list[i + 1] = '\uE1A3', ''
        if v == '\u103D':
            if html_list[i + 1] == '\u103E':
                html_list[i], html_list[i + 1] = '\uE1D1', ''
        if v == '\u102F':
            if html_list[i - 1] == '\u103E':
                html_list[i - 1], html_list[i] = '\uE1F2', ''
            if html_list[i - 2] == '\u103E':
                html_list[i - 2], html_list[i] = '\uE1F2', ''
        if v == '\u1030':
            if html_list[i - 1] == '\u103E':
                html_list[i - 1], html_list[i] = '\uE430', ''
            if html_list[i - 2] == '\u103E':
                html_list[i - 2], html_list[i] = '\uE430', ''

    # Virama(Subjoined Consonants: က္က, မ္မ, န္တ, etc.) character substitutions
    for i, v in enumerate(html_list):
        if v == '\u1039':
            if html_list[i - 1] == '\u103A' and html_list[i - 2] == '\u1004':
                html_list[i - 2], html_list[i - 1], html_list[i] = '', '', '\uE390'
                if html_list[i + 1] == '\u103C':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE1B6', html_list[i + 2], html_list[i]
                elif html_list[i + 1] == '\uE1B2':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE1B7', html_list[i + 2], html_list[i]
                else:
                    html_list[i], html_list[i + 1] = html_list[i + 1], html_list[i]
            else:
                if html_list[i + 1] == '\u1000': html_list[i], html_list[i + 1] = '\uE000', ''
                if html_list[i + 1] == '\u1001': html_list[i], html_list[i + 1] = '\uE001', ''
                if html_list[i + 1] == '\u1002': html_list[i], html_list[i + 1] = '\uE002', ''
                if html_list[i + 1] == '\u1003': html_list[i], html_list[i + 1] = '\uE003', ''

                if html_list[i + 1] == '\u1005': html_list[i], html_list[i + 1] = '\uE005', ''
                if html_list[i + 1] == '\u1006': html_list[i], html_list[i + 1] = '\uE006', ''
                if html_list[i + 1] == '\u1007': html_list[i], html_list[i + 1] = '\uE007', ''
                if html_list[i + 1] == '\u1008': html_list[i], html_list[i + 1] = '\uE008', ''

                if html_list[i + 1] == '\u100A': html_list[i], html_list[i + 1] = '\uE00A', ''
                if html_list[i + 1] == '\u100B': html_list[i], html_list[i + 1] = '\uE00B', ''
                if html_list[i + 1] == '\u100C': html_list[i], html_list[i + 1] = '\uE00C', ''
                if html_list[i - 1] == '\u100F' and html_list[i + 1] == '\u100D':
                    html_list[i - 1], html_list[i], html_list[i + 1] = '\uE105', '', ''
                elif html_list[i + 1] == '\u100D':
                    html_list[i], html_list[i + 1] = '\uE00D', ''
                if html_list[i + 1] == '\u100E': html_list[i], html_list[i + 1] = '\uE00E', ''
                if html_list[i + 1] == '\u100F': html_list[i], html_list[i + 1] = '\uE00F', ''

                if html_list[i + 1] == '\u1010': html_list[i], html_list[i + 1] = '\uE010', ''
                if html_list[i + 1] == '\u1011': html_list[i], html_list[i + 1] = '\uE011', ''
                if html_list[i + 1] == '\u1012': html_list[i], html_list[i + 1] = '\uE012', ''
                if html_list[i + 1] == '\u1013': html_list[i], html_list[i + 1] = '\uE013', ''
                if html_list[i + 1] == '\u1014': html_list[i], html_list[i + 1] = '\uE014', ''
                if html_list[i + 1] == '\u1015': html_list[i], html_list[i + 1] = '\uE015', ''
                if html_list[i + 1] == '\u1016': html_list[i], html_list[i + 1] = '\uE016', ''
                if html_list[i + 1] == '\u1017': html_list[i], html_list[i + 1] = '\uE017', ''
                if html_list[i + 1] == '\u1018': html_list[i], html_list[i + 1] = '\uE018', ''
                if html_list[i + 1] == '\u1019': html_list[i], html_list[i + 1] = '\uE019', ''

                if html_list[i + 1] == '\u101C': html_list[i], html_list[i + 1] = '\uE01C', ''
                if html_list[i + 1] == '\u101E': html_list[i], html_list[i + 1] = '\uE01E', ''
                if html_list[i + 1] == '\u101F': html_list[i], html_list[i + 1] = '\uE553', ''
                if html_list[i + 1] == '\u1021': html_list[i], html_list[i + 1] = '\uE021', ''

                if html_list[i + 2] == '\u102F': html_list[i + 2] = '\uE2F1'
                if html_list[i + 2] == '\u1030': html_list[i + 2] = '\uE2F2'
                if html_list[i - 1] == '\u1014': html_list[i - 1] = '\uE107'

    # 'KinZi'(Subjoined Nga: င်္စ, င်္ဃ, etc.) variant substitutions
    for i, v in enumerate(html_list):
        if v == '\uE390':
            if html_list[i + 1] == '\u103B':
                if html_list[i + 2] == '\u102E':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE392', html_list[i + 1], ''
                if html_list[i + 2] == '\u102D':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE391', html_list[i + 1], ''
                if html_list[i + 2] == '\u1032':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE396', html_list[i + 1], ''
                if html_list[i + 2] == '\u1036':
                    html_list[i], html_list[i + 1], html_list[i + 2] = '\uE393', html_list[i + 1], ''
            else:
                if html_list[i + 1] == '\u102E':
                    html_list[i], html_list[i + 1] = '\uE392', ''
                if html_list[i + 1] == '\u102D':
                    html_list[i], html_list[i + 1] = '\uE391', ''
                if html_list[i + 1] == '\u1032':
                    html_list[i], html_list[i + 1] = '\uE396', ''
                if html_list[i + 1] == '\u1036':
                    html_list[i], html_list[i + 1] = '\uE393', ''

    # 'YaYit' variant substitutions
    for i, v in enumerate(html_list):
        if v == '\u103C':
            if html_list[i + 2] in ['\u102D', '\u102E', '\u1032']:
                html_list[i] = '\uE1B6'
            if html_list[i + 2] == '\u103D':
                html_list[i] = '\uE1BB'
                if html_list[i + 3] in ['\u102D', '\u102E', '\u1032']:
                    html_list[i] = '\uE1B6'
        if v == '\uE1B2':
            if html_list[i + 2] in ['\u102D', '\u102E', '\u1032']:
                html_list[i] = '\uE1B7'
            if html_list[i + 2] == '\u103D':
                html_list[i] = '\uE1BC'
                if html_list[i + 3] in ['\u102D', '\u102E', '\u1032']:
                    html_list[i] = '\uE1B7'

    reshape_html = ''.join(map(str, html_list))
    return reshape_html
