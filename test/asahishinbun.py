import unittest
import re
from bs4 import BeautifulSoup as bs
from tenseijingoscraper import asahishinbun, userinfo
from tenseijingoscraper.scraper import AsahiShinbunScraper


class TestAsahishinbun(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_id = userinfo.id
        cls.user_pw = userinfo.password
        cls.obj = AsahiShinbunScraper(cls.user_id, cls.user_pw)
        cls.test_url = 'https://digital.asahi.com/articles/DA3S14297045.html'

    def test_convert_url(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        pattern = r'^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        self.assertRegex(asahishinbun.convert_url(url), pattern)

    def test_making_html(self):
        results = self.obj.get_contents_from_url(self.test_url)
        content_result = self.obj.convert_content_bs_to_dict(results)
        result = asahishinbun.convert_to_html(content_result)
        # result should be formatted by Head(H1, H3) and body
        content = bs(result, 'html.parser')
        self.assertGreater(len(content.find_all('head')), 0, "There's no head")
        self.assertGreater(len(content.find_all('body')), 0, "There's no body")
        # encoding
        char_re = re.compile(r"(?is)content=[\"'].*?;\s*charset=(.*?)[\"']")
        chk_result = char_re.search(result)
        self.assertTrue('utf-8' in chk_result.group())


if __name__ == '__main__':
    unittest.main()
