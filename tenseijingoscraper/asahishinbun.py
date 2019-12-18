import re

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