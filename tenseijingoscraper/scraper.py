# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from tenseijingoscraper import asahishinbun
from tenseijingoscraper.utils import DateHandling


def get_contents_from_url(url: str):
    """
    URLから天声人語コンテンツを取得する
    :param url: str
        コンテンツ取得対象のURL
    :return: BeautifulSoup
        コンテンツ
    """
    if url:
        with asahishinbun.AsahiSession.open_session() as s:
            res = s.get(url)
            if res.status_code != 200:
                raise ConnectionError
            res.encoding = res.apparent_encoding
            return bs(res.text, 'html.parser')
    else:
        raise ValueError


def get_contents_from_urls(urls: list):
    """
    (deprecated) URLのリストから天声人語コンテンツを取得する
    :param urls: list
        コンテンツ取得対象のURL
    :return: list[BeautifulSoup]
        コンテンツ
    """
    if urls:
        with asahishinbun.AsahiSession.open_session() as s:
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


def convert_content_bs_to_dict(url):
    from datetime import datetime
    soup = get_contents_from_url(url)
    dic_result = {
          'title': soup.findAll('h1')[0].text,
          'content': soup.findAll('div', attrs={'class', 'ArticleText'})[0].text,
          'datetime': str(DateHandling.convert_to_date_object(soup.findAll('span', attrs={'class', 'UpdateDate'})[0].findAll()[0].attrs['datetime']))
          }
    return dic_result


def get_backnumber_list():
    soup = get_contents_from_url(asahishinbun.content_list_url)
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
