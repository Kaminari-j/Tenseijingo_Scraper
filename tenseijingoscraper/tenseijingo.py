# -*- coding: utf-8 -*-
import os
from tenseijingoscraper import userinfo, asahishinbun, scraper
from tenseijingoscraper.asahishinbun import AsahiSession
import tenseijingoscraper.utils as utils
from tenseijingoscraper.utils import DateHandling


def get_html_with_date(date1: str, date2: str = None, download_path: str = None):
    # When download_path is None, then set ./html as default
    if download_path is None:
        download_path = r'./html'

    # When download_path is set, make or check existence of `download_path` directory
    _prepared = utils.prepare_directory(download_path)
    if not _prepared:
        exit(1)

    print(f'Working Directory is {download_path}')

    try:
        # log-in https://digital.asahi.com with User Id and Password
        with AsahiSession(userinfo.id, userinfo.password).open_session() as s:
            # Get list of contents
            article_list = scraper.get_backnumber_list(s)
            # Make date list from contents
            list_of_dates = [dt for dt in article_list.keys()]
            list_of_dates.sort()
            # Create instance of utils.DateHandling class
            t_date = DateHandling(list_of_dates, date1, date2)

            # get index of start date and end date
            idx_from = list_of_dates.index(t_date.date_from)
            idx_to = list_of_dates.index(t_date.date_to) + 1

            for cDate in list_of_dates[idx_from:idx_to]:
                # Print day
                print(cDate, end=': ')
                # Get full path of the day
                html_file_full_path = utils.naming_file(download_path, cDate)
                # Check existence html file of the day
                if not os.path.exists(html_file_full_path):
                    # Make dict with a content of the day
                    content = scraper.convert_content_bs_to_dict(s, article_list[cDate]['url'])
                    # Make html(str) with dict of the day
                    html = asahishinbun.convert_to_html(content['title'], content['datetime'], content['content'])
                    # Make html file with html string
                    utils.create_file(html_file_full_path, html)
                    # Print result
                    print('Downloaded. ')
                else:
                    # Skip if file already exists
                    print('skipped.')
    except ConnectionError as e:
        print(e)


def run(f_date: str = None, t_date: str = None, download_path: str = None):
    from datetime import date
    if not f_date:
        f_date = date.today().strftime('%Y%m%d')
    get_html_with_date(f_date, t_date, download_path)
