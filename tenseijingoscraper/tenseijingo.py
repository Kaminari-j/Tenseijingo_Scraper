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
    print(f'Working Directory is {download_path}')

    # https://digital.asahi.com User Id and Password
    user_id = userinfo.id
    user_password = userinfo.password

    try:
        with AsahiSession(user_id, user_password).open_session() as s:
            # Get list of content
            article_list = scraper.get_backnumber_list(s)
            list_of_dates = [dt for dt in article_list.keys()]
            list_of_dates.sort()
            t_date = DateHandling(list_of_dates, date1, date2)

            idx_from = list_of_dates.index(t_date.date_from)
            idx_to = list_of_dates.index(t_date.date_to) + 1

            for cDate in list_of_dates[idx_from:idx_to]:
                print(cDate, end=': ')
                html_file_full_name = utils.making_file_name(download_path, cDate)
                if not os.path.exists(html_file_full_name):
                    content = scraper.convert_content_bs_to_dict(s, article_list[cDate]['url'])
                    html = asahishinbun.convert_to_html(content['title'], content['datetime'], content['content'])
                    utils.create_file(html_file_full_name, html)
                    print('Downloaded. ')
                else:
                    print('skipped.')
    except ConnectionError as e:
        print(e)


def run(f_date: str = None, t_date: str = None, download_path: str = None):
    from datetime import date
    if not f_date:
        f_date = date.today().strftime('%Y%m%d')
    get_html_with_date(f_date, t_date, download_path)
