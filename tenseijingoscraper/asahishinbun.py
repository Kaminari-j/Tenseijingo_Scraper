import re
import requests
from bs4 import BeautifulSoup as bs

login_url = 'https://digital.asahi.com/login/login.html'
content_list_url = 'https://www.asahi.com/news/tenseijingo.html'
login_info = {
        'jumpUrl': 'https://www.asahi.com/?',
        'ref': None,
        'login_id': None,
        'login_password': None
    }


def convert_url(url: str):
    """
    convert url(backnumber) to individual content url
    :param url: url from backnumber
    :type url: str
    :return: url of individual content
    :rtype: url
    """
    pattern = r'^/articles/(\d|\D)+\.html\?iref\=tenseijingo_backnumber$'
    if re.compile(pattern).search(url):
        return 'https://digital.asahi.com' + url.split('?')[0]
    else:
        raise ValueError('Invalid URL')


def convert_to_html(content: dict):
    html = '<!DOCTYPE html> \
                <html>\
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> \
                    <head>\
                        <h1>{0}</h1> \
                        <h3 align="right">{1}</h3>\
                    </head>\
                    <body> \
                        <p>{2}</p> \
                    </body>\
                </html>'.format(content['title'], str(content['datetime']), content['content'])
    return html


class AsahiSession:
    __LOGIN_INFO = login_info

    @property
    def id(self):
        return self.__LOGIN_INFO['login_id']

    @property
    def password(self):
        return self.__LOGIN_INFO['login_password']

    def __init__(self, login_id, login_password):
        self.__LOGIN_INFO['login_id'] = login_id
        self.__LOGIN_INFO['login_password'] = login_password

    @staticmethod
    def open_session():
        with requests.Session() as s:
            login_req = s.post(login_url, data=AsahiSession.__LOGIN_INFO)
            if login_req.status_code != 200:
                raise ConnectionError('Connection Failed')
            login_req.encoding = login_req.apparent_encoding
            soup = bs(login_req.text, 'html.parser')
            login_result = soup.findAll('ul', attrs={'class', 'Error'})
            if len(login_result) > 0:
                raise ConnectionError(str.strip(login_result[0].text))
            else:
                return s
