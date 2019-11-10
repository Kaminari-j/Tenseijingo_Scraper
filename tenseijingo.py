from modules import TenseijingoModule
import os


def get_html_with_date(dateFrom: str, dateTo: str):
    # Todo : Convert this method to module and make available query by date from to
    download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # https://digital.asahi.com User Id and Password
    user_id = 'rodney.joo@gmail.com'
    user_password = 'CBMjELnZjvw7h'

    s = TenseijingoModule(user_id, user_password)
    try:
        s.open_session()

        article_list = s.get_backnumber_list()

        dt_list = [dt for dt in article_list.keys()]
        dt_list.sort()
        idx_from = dt_list.index(dateFrom)
        idx_to = dt_list.index(dateTo) + 1

        # Todo:
        #   if there no from date or to date
        #       how to handle does dates which are inside range
        #       ex) dateFrom = '20191001', dateTo = '20191010'
        #           dt_list = ['20191005', '20191006', '20191007']

        for upload_date in dt_list[idx_from:idx_to]:
            print(upload_date)
            content_dic = article_list[upload_date]
            content = s.convert_content_bs_to_dict(content_dic['url'])
            content_date = content['datetime'].strftime("%Y%m%d")

            html_name = download_path + '/' + content_date + '.html'
            if not os.path.exists(html_name):
                print('Downloading.. ' + html_name.split('/')[-1])
                html = TenseijingoModule.making_html(content)
                with open(html_name, 'w') as f:
                    f.write(html)
                    f.close()
    except ConnectionError as e:
        print(e)


if __name__ == '__main__':
    get_html_with_date('20191001', '20191003')
