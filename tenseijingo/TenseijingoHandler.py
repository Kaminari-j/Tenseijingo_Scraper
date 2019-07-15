
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
    def convert_to_pdf(html: str):
        return html