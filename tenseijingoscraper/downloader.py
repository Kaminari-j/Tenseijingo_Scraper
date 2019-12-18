# -*- coding: utf-8 -*-
import os
from tenseijingoscraper import userinfo, asahishinbun
from tenseijingoscraper.scraper import AsahiShinbunScraper
from tenseijingoscraper import utils


def get_html_with_date(date1: str, date2=None, download_path=None):
    if download_path is None:
        download_path = r'./html'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # https://digital.asahi.com User Id and Password
    user_id = userinfo.id
    user_password = userinfo.password

    scraper = AsahiShinbunScraper(user_id, user_password)
    try:
        scraper.open_session()

        # Get list of content
        article_list = scraper.get_backnumber_list()
        list_of_dates = [dt for dt in article_list.keys()]
        list_of_dates.sort()
        t_date = utils.DateHandling(list_of_dates, date1, date2)
        list_of_dates = list_of_dates[list_of_dates.index(t_date.date_from):list_of_dates.index(t_date.date_to) + 1]

        print('{0}~{1}'.format(t_date.date_from, t_date.date_to))

        existing_check_list = list()
        for content_date in list_of_dates:
            if os.path.exists(utils.html_file_name(download_path, content_date)):
                existing_check_list.append([content_date, None])
            else:
                existing_check_list.append([content_date, article_list[content_date]['url']])

        download_urls = [[date, url] for date, url in existing_check_list if url is not None]
        if download_urls:
            contents = scraper.get_contents_from_urls(download_urls)
            for date, content in contents:
                content_dic = AsahiShinbunScraper.convert_content_bs_to_dict(content)
                html = asahishinbun.convert_to_html(content_dic)
                with open(utils.html_file_name(download_path, date), 'w') as f:
                    f.write(html)
                    f.close()

        for date, url in existing_check_list:
            print(date, end=': ')
            if url is None:
                print('skip')
            else:
                print('Download ')
    except ConnectionError as e:
        print(e)


def run():
    from datetime import date
    get_html_with_date(date.today().strftime('%Y%m%d'))
