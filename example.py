from tenseijingo import tenseijingo, ini
from tenseijingo.TenseijingoHandler import handler
import datetime
import pdfkit


if __name__ == '__main__':
    download_path = r'test/test_html'
    user = ini.User()
    s = tenseijingo(user.id, user.password)
    s.open()

    article_list = s.get_list()
    for article in article_list[1:10]:
        content = s.get_content(article)
        html = handler.making_html(content)

        fname = download_path + '/' + content['datetime'].strftime("%Y%m%d")

        with open(fname + '.html', 'w') as f:
            f.write(html)
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            # Todo : fix below phrase
            pdfkit.from_file(f, fname + '.pdf')
            # Todo : seperate making html (with session) and making pdf
            f.close()
