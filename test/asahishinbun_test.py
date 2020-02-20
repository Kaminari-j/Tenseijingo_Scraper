import unittest
import re
from bs4 import BeautifulSoup as bs
from tenseijingoscraper import asahishinbun, userinfo, scraper
from tenseijingoscraper.asahishinbun import AsahiSession

# Todo : User ID/Password 가 설정되어 있지 않는 경우에도 테스트를 할 수 있도록 할 것


class TestAsahishinbun(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_id = userinfo.id
        cls.user_pw = userinfo.password
        cls.obj = AsahiSession(cls.user_id, cls.user_pw)
        cls.s = cls.obj.open_session()
        cls.test_url = 'https://digital.asahi.com/articles/DA3S14297045.html'

    def test_convert_url(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        pattern = r'^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        self.assertRegex(asahishinbun.convert_url(url), pattern)

    def test_making_html(self):
        content_result = scraper.convert_content_bs_to_dict(self.s, self.test_url)
        result = asahishinbun.convert_to_html(content_result['title'], content_result['datetime'], content_result['content'])
        # result should be formatted by Head(H1, H3) and body
        content = bs(result, 'html.parser')
        self.assertGreater(len(content.find_all('head')), 0, "There's no head")
        self.assertGreater(len(content.find_all('body')), 0, "There's no body")
        # encoding
        char_re = re.compile(r"(?is)content=[\"'].*?;\s*charset=(.*?)[\"']")
        chk_result = char_re.search(result)
        self.assertTrue('utf-8' in chk_result.group())


class TestAsahiSession(unittest.TestCase):
    @unittest.skipIf(not userinfo.id and not userinfo.password, 'Userinfo not set')
    def test_open_session_ok(self):
        import requests
        s = AsahiSession(userinfo.id, userinfo.password).open_session()
        self.assertIsInstance(s, requests.Session)

    def test_open_session_ng(self):
        with self.assertRaises(ConnectionError):
            AsahiSession(None, None).open_session()


if __name__ == '__main__':
    unittest.main()
