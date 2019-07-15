from tenseijingo import tenseijingo, ini
from tenseijingo.TenseijingoHandler import handler
import datetime
import pdfkit
import os


if __name__ == '__main__':
    download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    user = ini.User()

    s = tenseijingo(user.id, user.password)
    try:
        s.open()

        article_list = s.get_list()
        for article in article_list[0:1]:
            content = s.get_content(article)
            content_date = content['datetime'].strftime("%Y%m%d")

            html_name = download_path + '/' + content_date + '.html'
            if not os.path.exists(html_name):
                print('Downloading.. ' + html_name.split('/')[-1])
                html = handler.making_html(content)
                with open(html_name, 'w') as f:
                    f.write(html)
                    #config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
                    # Todo : fix below phrase
                    #pdfkit.from_file(f, fname + '.pdf')
                    # Todo : seperate making html (with session) and making pdf
                    f.close()
    except ConnectionError as e:
        print(e)
    s.close()
