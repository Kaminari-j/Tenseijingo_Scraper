# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from tenseijingoscraper import asahishinbun
from tenseijingoscraper.utils import DateHandling


class AsahiShinbunScraper:
    __LOGIN_INFO = asahishinbun.login_info

    @property
    def id(self):
        return self.__LOGIN_INFO['login_id']

    @property
    def password(self):
        return self.__LOGIN_INFO['login_password']

    def __init__(self, login_id, login_password):
        self.__LOGIN_INFO['login_id'] = login_id
        self.__LOGIN_INFO['login_password'] = login_password

    def open_session(self):
        with requests.Session() as s:
            login_req = s.post(asahishinbun.login_url, data=self.__LOGIN_INFO)
            if login_req.status_code != 200:
                raise ConnectionError('Connection Failed')
            login_req.encoding = login_req.apparent_encoding
            soup = bs(login_req.text, 'html.parser')
            login_result = soup.findAll('ul', attrs={'class', 'Error'})
            if len(login_result) > 0:
                raise ConnectionError(str.strip(login_result[0].text))
            else:
                return s

    def get_contents_from_url(self, url: str):
        """
        URLから天声人語コンテンツを取得する
        :param url: str
            コンテンツ取得対象のURL
        :return: BeautifulSoup
            コンテンツ
        """
        if url:
            with self.open_session() as s:
                res = s.get(url)
                if res.status_code != 200:
                    raise ConnectionError
                res.encoding = res.apparent_encoding
                return bs(res.text, 'html.parser')
        else:
            raise ValueError

    def get_contents_from_urls(self, download_list: list):
        """
        (deprecated) URLのリストから天声人語コンテンツを取得する
        :param download_list: list[str, str]
            コンテンツの日付、URL
        :return: list[str, BeautifulSoup]
            コンテンツの日付、BeautifulSoup オブジェクト
        """
        if download_list:
            with self.open_session() as s:
                results = list()
                for date, url in download_list:
                    print('.', end='')
                    res = s.get(url)
                    if res.status_code != 200:
                        raise ConnectionError
                    res.encoding = res.apparent_encoding
                    results.append([date, bs(res.text, 'html.parser')])
                print('')
                return results
        else:
            raise ValueError

    @staticmethod
    def convert_content_bs_to_dict(obj: bs):
        return {
              'title': obj.findAll('h1')[0].text,
              'content': obj.findAll('div', attrs={'class', 'ArticleText'})[0].text,
              'datetime': DateHandling.convert_to_date_object(obj.findAll('time', attrs={'class', 'LastUpdated'})[0].attrs['datetime'])
              }

    def get_backnumber_list(self):
        soup = self.get_contents_from_url(asahishinbun.content_list_url)
        panels = soup.findAll('div', attrs={'class', 'TabPanel'})
        dic_article = dict()
        for panel in panels:
            list_items = panel.findAll('li')
            for item in list_items:
                _date = item['data-date']
                _title = item.findAll('em')[0].text
                _url = asahishinbun.convert_url(item.findAll('a')[0]['href'])

                dic_article[_date] = {'title': _title, 'url': _url}
        return dic_article if len(dic_article) > 0 else None
