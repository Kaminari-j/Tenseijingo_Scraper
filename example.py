from tenseijingo import tenseijingo
import os


if __name__ == '__main__':
    download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # https://digital.asahi.com User Id and Password
    user_id = ''
    user_password = ''

    s = tenseijingo(user_id, user_password)
    try:
        s.open_session()

        article_list = s.get_list()
        for upload_date, content_dic in article_list.items():
            content = s.convert_content_to_dict(content_dic['url'])
            content_date = content['datetime'].strftime("%Y%m%d")

            html_name = download_path + '/' + content_date + '.html'
            if not os.path.exists(html_name):
                print('Downloading.. ' + html_name.split('/')[-1])
                html = tenseijingo.making_html(content)
                with open(html_name, 'w') as f:
                    f.write(html)
                    f.close()
    except ConnectionError as e:
        print(e)
