import unittest
from tenseijingo import tenseijingo, ini, TenseijingoHandler as handler
import re


class TestTenseijingo_Init(unittest.TestCase):
    def test_1_should_be_placed_property(self):
        id = 'testid'
        pswd = 'testpswd'
        result = tenseijingo(id, pswd)
        self.assertEqual(result.id, id)
        self.assertEqual(result.password, pswd)

    def test_2_should_be_raise_error_when_value_none(self):
        with self.assertRaises(ValueError):
            tenseijingo(None, 'Test')
        with self.assertRaises(ValueError):
            tenseijingo('Test', None)
        with self.assertRaises(ValueError):
            tenseijingo(None, None)


class TestTenseijingo_Open_Session(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()

    def test_1_when_success(self):
        self.obj = tenseijingo(self.user.id, self.user.password)
        self.assertIsNotNone(self.obj._tenseijingo__open_session())

    def test_2_when_fail(self):
        self.obj = tenseijingo('test', 'test')
        with self.assertRaises(ConnectionError):
            self.obj._tenseijingo__open_session()


class TestTenseijingo_Get_Contents_From_Url(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)

    def test_when_success(self):
        from bs4 import BeautifulSoup
        self.assertIsInstance(
            self.obj._tenseijingo__get_contents_from_url('https://digital.asahi.com/articles/DA3S14049498.html'),
            BeautifulSoup
        )

    def test_when_failed_to_get_contents(self):
        with self.assertRaises(ConnectionError):
            self.obj._tenseijingo__get_contents_from_url('https://digital.asahi.com/articles/DA123.html')

    def test_when_url_is_none(self):
        with self.assertRaises(ValueError):
            self.obj._tenseijingo__get_contents_from_url('')


class TestTenseijingo_get_content(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.result_ok = cls.obj.get_content('https://digital.asahi.com/articles/DA3S14049498.html')

    def test_1_result_should_be_not_none(self):
        self.assertIsNotNone(self.result_ok)

    def test_2_result_should_be_instance_of_dict(self):
        self.assertIsInstance(self.result_ok, dict)

    def test_3_result_should_containing_elements(self):
        elements = ('title', 'content', 'datetime')
        for element in elements:
            self.assertIsNotNone(self.result_ok[element])

    def test_4_should_raise_when_failed_to_load(self):
        with self.assertRaises(Exception):
            self.obj.get_content('https://digital.asahi.com/articles/DA3S14098.html')

    def test_5_check_type(self):
        elements = ('title', 'content')
        for element in elements:
            self.assertEqual(type(self.result_ok[element]), str)
        self.assertEqual(type('datetime'), str)


class TestTenseijingo_get_list(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.result = cls.obj.get_list()

    def test_1_result_is_not_none(self):
        self.assertIsNotNone(self.result)

    def test_2_count_of_result_is_larger(self):
        count = len(self.result)
        self.assertTrue(1 <= count <= 122)

    def test_3_elements_of_dict_level1(self):
        date_pattern = '^20\d\d[0-1]{1}\d[0-3]\d$'
        for item in self.result:
            # is element string
            self.assertIsInstance(item, str)
            # is element 8digits
            self.assertEqual(len(item), 8)
            # is element date
            self.assertRegex(item, date_pattern)

    def test_4_elements_of_dict_level2(self):
        title_pattern = '\w+'
        url_pattern = '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        for item in self.result.values():
            for key, value in item.items():
                if key == 'title':
                    self.assertRegex(value, title_pattern)
                if key == 'url':
                    # https://digital.asahi.com/articles/DA3S14049498.html
                    self.assertRegex(value, url_pattern)


class TestTenseijingo_convert_url(unittest.TestCase):
    def test_convert_url(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        pattern = '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        result = tenseijingo._tenseijingo__convert_url(url)
        self.assertRegex(result, pattern)


class TestTenseijingo_check_url(unittest.TestCase):
    def test_1_when_correct(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        result = tenseijingo._tenseijingo__check_url(url)
        self.assertTrue(result)

    def test_2_when_incorrect(self):
        url = 'javascript:void(0)'
        result = tenseijingo._tenseijingo__check_url(url)
        self.assertFalse(result)


class Test_Making_html(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.content_result = cls.obj.get_content('https://digital.asahi.com/articles/DA3S14049498.html')

    def test_result_is_not_none(self):
        result = handler.making_html(self.content_result)
        self.assertIsNotNone(result)

    def test_check_results_form(self):
        from bs4 import BeautifulSoup as bs

        # result should be formatted by Head(H1, H3) and body
        result = handler.making_html(self.content_result)
        content = bs(result)
        head = content.find_all('head')
        body = content.find_all('body')

        self.assertNotEqual(len(head), 0, "There's no head")
        self.assertNotEqual(len(body), 0, "There's no body")


class Test_ConvertToPdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_file = './test_html/test.html'

    def test_ok_pattern(self):
        result = handler.convert_to_pdf(self.html_file)
        self.assertIsNotNone(result)
        # Todo: check if file exists

    # Todo: Make testcase by OS


if __name__ == '__main__':
    unittest.main()
