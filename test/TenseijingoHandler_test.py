import unittest
from tenseijingo import ini, tenseijingo
from tenseijingo.TenseijingoHandler import handler
from bs4 import BeautifulSoup as bs


class Test_Making_html(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.obj.open()
        cls.content_result = cls.obj.get_content('https://digital.asahi.com/articles/DA3S14049498.html')

    def test_result_is_not_none(self):
        result = handler.making_html(self.content_result)
        self.assertIsNotNone(result)

    def test_check_results_form(self):
        # result should be formatted by Head(H1, H3) and body
        result = handler.making_html(self.content_result)
        content = bs(result)
        head = content.find_all('head')
        body = content.find_all('body')

        self.assertNotEqual(len(head), 0, "There's no head")
        self.assertNotEqual(len(body), 0, "There's no body")

    @classmethod
    def tearDownClass(cls):
        cls.obj.close()


class Test_ConvertToPdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_file = './test_html/test.html'

    def test_ok_pattern(self):
        result = handler.convert_to_pdf(self.html_file)
        self.assertIsNotNone(result)

