import unittest
from tenseijingo import TenseijingoModule
import userinfo


class ini:
    class User:
        id = userinfo.id
        password = userinfo.password


class Test_Init(unittest.TestCase):
    def test_1_should_be_placed_property(self):
        id = 'testid'
        pswd = 'testpswd'
        result = TenseijingoModule(id, pswd)
        self.assertEqual(result.id, id)
        self.assertEqual(result.password, pswd)

    def test_2_should_be_raise_error_when_value_none(self):
        with self.assertRaises(ValueError):
            TenseijingoModule(None, 'Test')
        with self.assertRaises(ValueError):
            TenseijingoModule('Test', None)
        with self.assertRaises(ValueError):
            TenseijingoModule(None, None)


class Test_Open_Session(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()

    def test_1_when_success(self):
        self.obj = TenseijingoModule(self.user.id, self.user.password)
        self.assertIsNotNone(self.obj.open_session())

    def test_2_when_fail(self):
        self.obj = TenseijingoModule('test', 'test')
        with self.assertRaises(ConnectionError):
            self.obj.open_session()


class Test_Get_Contents_From_Url(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)

    def test_when_success(self):
        from bs4 import BeautifulSoup
        self.assertIsInstance(
            self.obj.get_contents_from_url('https://digital.asahi.com/articles/DA3S14049498.html'),
            BeautifulSoup
        )


class Test_Get_Contents_From_Urls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)

    def test_when_success(self):
        from bs4 import BeautifulSoup
        results = self.obj.get_contents_from_urls(['https://digital.asahi.com/articles/DA3S14049498.html'])
        self.assertIsInstance(results, list)
        for res in results:
            self.assertIsInstance(res, BeautifulSoup)

    def test_when_failed_to_get_contents(self):
        with self.assertRaises(ConnectionError):
            self.obj.get_contents_from_urls(['https://digital.asahi.com/articles/DA123.html'])

    def test_when_url_is_none(self):
        with self.assertRaises(ValueError):
            self.obj.get_contents_from_urls([''])


class Test_convert_content_bs_to_dict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)
        cls.result_ok = cls.obj.convert_content_bs_to_dict('https://digital.asahi.com/articles/DA3S14049498.html')

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
            self.obj.convert_content_bs_to_dict('https://digital.asahi.com/articles/DA3S14098.html')

    def test_5_check_type(self):
        elements = ('title', 'content')
        for element in elements:
            self.assertEqual(type(self.result_ok[element]), str)
        self.assertEqual(type('datetime'), str)


class Test_get_backnumber_list(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)
        cls.result = cls.obj.get_backnumber_list()

    def test_1_result_is_not_none(self):
        self.assertIsNotNone(self.result)

    def test_2_result_is_instance_of(self):
        self.assertIsInstance(self.result, dict)

    def test_3_count_of_result_is(self):
        count = len(self.result)
        self.assertTrue(1 <= count <= 122)

    def test_4_elements_of_dict_level1(self):
        date_pattern = '^20\d\d[0-1]{1}\d[0-3]\d$'
        for item in self.result:
            # is element string
            self.assertIsInstance(item, str)
            # is element 8digits
            self.assertEqual(len(item), 8)
            # is element date
            self.assertRegex(item, date_pattern)

    def test_5_elements_of_dict_level2(self):
        title_pattern = '\w+'
        url_pattern = '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        for item in self.result.values():
            for key, value in item.items():
                if key == 'title':
                    self.assertRegex(value, title_pattern)
                if key == 'url':
                    # https://digital.asahi.com/articles/DA3S14049498.html
                    self.assertRegex(value, url_pattern)


class Test_convert_url(unittest.TestCase):
    good_url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
    bad_url = 'javascript:void(0)'

    def test_when_url_ok(self):
        pattern = r'^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        result = TenseijingoModule.convert_url(self.good_url)
        self.assertRegex(result, pattern)

    def test_when_url_ng(self):
        with self.assertRaises(ValueError):
            TenseijingoModule.convert_url(self.bad_url)


class Test_Making_html(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)
        cls.content_result = cls.obj.convert_content_bs_to_dict('https://digital.asahi.com/articles/DA3S14049498.html')

    def test_result_is_not_none(self):
        result = TenseijingoModule.making_html(self.content_result)
        self.assertIsNotNone(result)

    def test_check_results_form(self):
        from bs4 import BeautifulSoup as bs

        # result should be formatted by Head(H1, H3) and body
        result = TenseijingoModule.making_html(self.content_result)
        content = bs(result, 'html.parser')
        head = content.find_all('head')
        body = content.find_all('body')

        self.assertNotEqual(len(head), 0, "There's no head")
        self.assertNotEqual(len(body), 0, "There's no body")

    def test_encoding(self):
        import re
        pattern = r"(?is)content=[\"'].*?;\s*charset=(.*?)[\"']"
        char_re = re.compile(pattern)
        html_result = TenseijingoModule.making_html(self.content_result)
        chk_result = char_re.search(html_result)
        self.assertIsNotNone(chk_result)
        self.assertTrue('utf-8' in chk_result.group())


if __name__ == '__main__':
    unittest.main()
