# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime


class tenseijingo:
    __LOGIN_INFO = {
        'jumpUrl': 'https://www.asahi.com/?',
        'ref': None,
        'login_id': None,
        'login_password': None
    }

    @property
    def id(self):
        return self.__LOGIN_INFO['login_id']

    @property
    def password(self):
        return self.__LOGIN_INFO['login_password']

    def __init__(self, id, password):
        if id is None or password is None:
            raise ValueError("ID or Password shouldn't be None")
        self.__LOGIN_INFO['login_id'] = id
        self.__LOGIN_INFO['login_password'] = password

    def open_session(self):
        __login_url = 'https://digital.asahi.com/login/login.html'
        with requests.Session() as s:
            login_req = s.post(__login_url, data=self.__LOGIN_INFO)
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
        if url:
            with self.open_session() as s:
                # https://digital.asahi.com/articles/DA3S14049498.html
                res = s.get(url)
                if res.status_code != 200:
                    raise ConnectionError
                res.encoding = res.apparent_encoding
                return bs(res.text, 'html.parser')
        else:
            raise ValueError

    def get_contents_from_urls(self, urls: list):
        if urls:
            with self.open_session() as s:
                results = list()
                for url in urls:
                    res = s.get(url)
                    if res.status_code != 200:
                        raise ConnectionError
                    res.encoding = res.apparent_encoding
                    results.append(bs(res.text, 'html.parser'))
                return results
        else:
            raise ValueError

    def get_content(self, url):
        soup = self.get_contents_from_url(url)
        dic_result = {
                  'title': soup.findAll('h1')[0].text,
                  'content': soup.findAll('div', attrs={'class', 'ArticleText'})[0].text,
                  'datetime': datetime.datetime.strptime(soup.findAll('time', attrs={'class','LastUpdated'})[0].attrs['datetime'], "%Y-%m-%dT%H:%M")
                  }
        return dic_result

    def get_list(self):
        __list_url = 'https://www.asahi.com/news/tenseijingo.html'
        soup = self.get_contents_from_url(__list_url)
        panels = soup.findAll('div', attrs={'class', 'TabPanel'})
        dic_article = dict()
        for panel in panels:
            list_items = panel.findAll('li')
            for item in list_items:
                _date = item['data-date']
                _title = item.findAll('em')[0].text
                _url = tenseijingo.convert_url(item.findAll('a')[0]['href'])

                dic_article[_date] = {'title': _title, 'url': _url}
        return dic_article if len(dic_article) > 0 else None

    @staticmethod
    def convert_url(url: str):
        if tenseijingo.check_url(url):
            return 'https://digital.asahi.com' + url.split('?')[0]
        else:
            raise ValueError

    @staticmethod
    def check_url(url: str):
        pattern = '^/articles/(\d|\D)+\.html\?iref\=tenseijingo_backnumber$'
        return True if re.compile(pattern).search(url) else False

    @staticmethod
    def making_html(content: dict):
        html = '<!DOCTYPE html> \
                    <html>\
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> \
                        <head>\
                            <h1>' + content['title'] + '</h1> \
                            <h3 align="right">' + str(content['datetime']) + '</h3>\
                        </head>\
                        <body> \
                            <p>' + content['content'] + '</p> \
                        </body>\
                    </html>'
        return html


if __name__ == '__main__':
    user_id = ''
    user_password = ''
    s = tenseijingo(user_id, user_password)
    result = s.get_list()
    #result = s.get_content('https://digital.asahi.com/articles/DA3S14049498.html')

