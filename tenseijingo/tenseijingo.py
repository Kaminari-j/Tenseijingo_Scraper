# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime
import ini


class tenseijingo:
    __LOGIN_INFO = {
        'jumpUrl': 'https://www.asahi.com/?',
        'ref': None,
        'login_id': None,
        'login_password': None
    }
    __session = None
    __login_url = 'https://digital.asahi.com/login/login.html'
    __list_url = 'https://www.asahi.com/news/tenseijingo.html'

    @property
    def session(self):
        return self.__session

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

    def __open_session(self):
        with requests.Session() as s:
            login_req = s.post(self.__login_url, data=self.__LOGIN_INFO)
            if login_req.status_code != 200:
                raise ConnectionError('Connection Failed')
            login_req.encoding = login_req.apparent_encoding
            soup = bs(login_req.text, 'html.parser')
            login_result = soup.findAll('ul', attrs={'class', 'Error'})
            if len(login_result) > 0:
                raise ConnectionError(str.strip(login_result[0].text))
            else:
                self.__session = s

    # requests.Session
    def __close_session(self):
        if self.__session:
            self.__session.close()
            # Todo: Is it work?
            self.__session = None

    def get_content(self, url):
        # https://digital.asahi.com/articles/DA3S14049498.html
        res = self.session.get(url)
        if res.status_code != 200:
            raise Exception('Connection Failed')
        soup = bs(res.text, 'html.parser')
        res.encoding = res.apparent_encoding

        result = {'title': soup.findAll('h1')[0].text,
                  'content': soup.findAll('div', attrs={'class', 'ArticleText'})[0].text,
                  'datetime': datetime.datetime.strptime(soup.findAll('time', attrs={'class','LastUpdated'})[0].attrs['datetime'], "%Y-%m-%dT%H:%M")
                  }
        return result

    def get_list(self):
        list_page = self.__list_url
        res = self.__session.get(list_page)
        if res.status_code != 200:
            raise Exception('Connection Failed')
        res.encoding = res.apparent_encoding
        soup = bs(res.text, 'html.parser')
        result = list()
        for link in soup.findAll('div', attrs={'class', 'TabMod'})[0].findAll({'a', 'href'}):
            attr = link.attrs['href']
            if tenseijingo.__check_url(attr):
                result.append(tenseijingo.__convert_url(attr))
        return result if len(result) > 0 else None

    @staticmethod
    def __convert_url(url: str):
        return 'https://digital.asahi.com' + url.split('?')[0]

    @staticmethod
    def __check_url(url: str):
        pattern = '^/articles/(\d|\D)+\.html\?iref\=tenseijingo_backnumber$'
        return True if re.compile(pattern).search(url) else False


class TenseijingoHandler():
    @staticmethod
    def making_html(content: dict):
        html = '<!DOCTYPE html> \
                    <html>\
                        <head>\
                            <h1>' + content['title'] + '</h1> \
                            <h3 align="right">' + str(content['datetime']) + '</h3>\
                        </head>\
                        <body> \
                            <p>' + content['content'] + '</p> \
                        </body>\
                    </html>'
        return html

    @staticmethod
    def convert_to_pdf(html):
        import os
        import pdfkit

        html_base = os.path.splitext(html)[0]
        pdf_out = html_base + '.pdf'

        options = {
            'page-size': 'A4',
            'margin-top': '0.1in',
            'margin-right': '0.1in',
            'margin-bottom': '0.1in',
            'margin-left': '0.1in',
            'encoding': "shift_jis",
            'no-outline': None
        }

        pdfkit.from_file(html, pdf_out, options=options)
        return pdf_out


if __name__ == '__main__':
    user = ini.User()
    s = tenseijingo(user.id, user.password)
    s.__open_session()
    result = s.get_content('https://digital.asahi.com/articles/DA3S14049498.html')

    print(result)
