import unittest
from tenseijingo import tenseijingo, ini
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


class TestTenseijingo_Open(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()

    def test_1_when_success(self):
        self.obj = tenseijingo(self.user.id, self.user.password)
        self.obj.open()
        self.assertIsNotNone(self.obj.session)

    def test_2_when_fail(self):
        self.obj = tenseijingo('test', 'test')
        with self.assertRaises(Exception):
            self.obj.open()

    def tearDown(self):
        if self.obj.session:
            self.obj.session.close()


class TestTenseijingo_get_content(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.obj.open()
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

        import datetime
        self.assertEqual(type('datetime'), datetime)


class TestTenseijingo_get_list(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.user = ini.User()
        cls.obj = tenseijingo(cls.user.id, cls.user.password)
        cls.obj.open()
        cls.result = cls.obj.get_list()

    def test_1_result_is_not_none(self):
        self.assertIsNotNone(self.result)

    def test_2_count_of_result_is_larger(self):
        count = len(self.result)
        self.assertTrue(1 <= count <= 122)

    def test_3_elements_of_list_are_string(self):
        for item in self.result:
            self.assertIsInstance(item, str)

    def test_4_elements_of_list_are_url(self):
        # https://digital.asahi.com/articles/DA3S14049498.html
        pattern = '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        for item in self.result:
            self.assertIsNotNone(re.compile(pattern).match(item))

    @classmethod
    def tearDownClass(cls):
        cls.obj.close()


class TestTenseijingo_convert_url(unittest.TestCase):
    def test_convert_url(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        pattern = '^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        result = tenseijingo.convert_url(url)
        self.assertRegex(result, pattern)


class TestTenseijingo_check_url(unittest.TestCase):
    def test_1_when_correct(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        result = tenseijingo.check_url(url)
        self.assertTrue(result)

    def test_2_when_incorrect(self):
        url = 'javascript:void(0)'
        result = tenseijingo.check_url(url)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
