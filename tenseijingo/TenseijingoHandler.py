import pdfkit
import sys
import os

class handler():
    @staticmethod
    def making_html(content: dict):
        html = '<!DOCTYPE html> \
                    <html>\
                        <head>\
                            <h1>' + content['title'] + '</h1> \
                            <h3 align="right">' + str(content['datetime']) + '</h3>\
                        </head>\
                        <body> \
                            <p>' + content['content'] + '</p> \
                        </body>\
                    </html>'
        return html

    # Todo : html to pdf converter
    @staticmethod
    def convert_to_pdf(html):
        html_base = os.path.splitext(html)[0]
        pdf_out = html_base + '.pdf'

        options = {
            'page-size': 'A4',
            'margin-top': '0.1in',
            'margin-right': '0.1in',
            'margin-bottom': '0.1in',
            'margin-left': '0.1in',
            'encoding': "shift_jis",
            'no-outline': None
        }

        pdfkit.from_file(html, pdf_out, options=options)
