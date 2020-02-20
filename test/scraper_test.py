import unittest
from bs4 import BeautifulSoup as bs
from tenseijingoscraper import userinfo, scraper
from tenseijingoscraper.asahishinbun import AsahiSession


class TestScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_id = userinfo.id
        cls.user_pw = userinfo.password
        cls.obj = AsahiSession(cls.user_id, cls.user_pw)
        cls.s = cls.obj.open_session()
        cls.test_url = 'https://digital.asahi.com/articles/DA3S14297045.html'
        cls.test_url2 = 'https://digital.asahi.com/articles/DA3S14295448.html'

    def test_get_contents_from_url(self):
        self.assertIsInstance(
            scraper.get_contents_from_url(self.s, self.test_url),
            bs
        )

    def test_convert_content_bs_to_dict(self):
        result_ok = scraper.convert_content_bs_to_dict(self.s, self.test_url)
        # result_should_be_instance_of_dict
        self.assertIsInstance(result_ok, dict)
        # check element's type
        import datetime
        self.assertIsInstance(result_ok['title'], str)
        self.assertIsInstance(result_ok['content'], str)
        self.assertIsInstance(result_ok['datetime'], str)

    def test_get_backnumber_list(self):
        result = scraper.get_backnumber_list(self.s)
        self.assertIsInstance(result, dict)
        # count_of_result
        self.assertTrue(1 <= len(result) <= 122)
        # elements_of_dict_level1
        for item in result:
            # is element string
            self.assertIsInstance(item, str)
            # is element 8digits
            self.assertEqual(len(item), 8)
            # is element date
            self.assertRegex(item, '^20\d\d[0-1]{1}\d[0-3]\d$')
        # elements_of_dict_level2
        for item in result.values():
            for key, value in item.items():
                if key == 'title':
                    self.assertRegex(value, '\w+')
                if key == 'url':
                    self.assertRegex(value, '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$')


if __name__ == '__main__':
    unittest.main()
