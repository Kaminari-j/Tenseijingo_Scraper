from tenseijingo import tenseijingo, TenseijingoHandler as handler
import datetime
import pdfkit
import os


if __name__ == '__main__':
    download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Asahi login info
    user_id = ''
    user_password = ''

    s = tenseijingo(user_id, user_password)
    try:
        s.__open_session()

        article_list = s.get_list()
        for article in article_list[0:]:
            content = s.get_content(article)
            content_date = content['datetime'].strftime("%Y%m%d")

            html_name = download_path + '/' + content_date + '.html'
            if not os.path.exists(html_name):
                print('Downloading.. ' + html_name.split('/')[-1])
                html = handler.making_html(content)
                with open(html_name, 'w') as f:
                    f.write(html)
                    f.close()
                handler.convert_to_pdf(html_name)
    except ConnectionError as e:
        print(e)
    s.__close_session()
