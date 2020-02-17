# -*- coding: utf-8 -*-
import os
from tenseijingoscraper import userinfo, asahishinbun, scraper
from tenseijingoscraper.asahishinbun import AsahiSession
import tenseijingoscraper.utils as utils
from tenseijingoscraper.utils import DateHandling


def get_html_with_date(date1: str, date2: str = None, download_path: str = None):
    if download_path is None:
        download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # https://digital.asahi.com User Id and Password
    user_id = userinfo.id
    user_password = userinfo.password

    s = AsahiSession(user_id, user_password)
    try:
        s.open_session()

        # Get list of content
        article_list = scraper.get_backnumber_list()
        list_of_dates = [dt for dt in article_list.keys()]
        list_of_dates.sort()
        t_date = DateHandling(list_of_dates, date1, date2)
        
        idx_from = list_of_dates.index(t_date.date_from)
        idx_to = list_of_dates.index(t_date.date_to) + 1

        for content_date in list_of_dates[idx_from:idx_to]:
            print(content_date, end=': ')
            html_name = utils.making_file_name(download_path, content_date)
            if not os.path.exists(html_name):
                contents = article_list[content_date]
                content = scraper.convert_content_bs_to_dict(contents['url'])

                print('Downloading.. ' + html_name.split('/')[-1])
                html = asahishinbun.convert_to_html(content)
                with open(html_name, 'w') as f:
                    f.write(html)
                    f.close()
            else:
                print('skip')
    except ConnectionError as e:
        print(e)


def run(f_date: str = None, t_date: str = None, download_path: str = None):
    from datetime import date
    if not f_date:
        f_date = date.today().strftime('%Y%m%d')
    get_html_with_date(f_date, t_date, download_path)
