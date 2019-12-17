import unittest
from bs4 import BeautifulSoup as bs
import re
import tenseijingo
from tenseijingo import TenseijingoModule, TenseijingoDate
import userinfo


class ini:
    class User:
        id = userinfo.id
        password = userinfo.password


class TestTenseijingoDate(unittest.TestCase):
    def test_get_date_n_days_ago(self):
        self.assertEqual(TenseijingoDate.get_date_n_days_ago('20191003', 2), '20191001')

    def test_rearrange_date_arguments(self):
        datefrom, dateto = TenseijingoDate.rearrange_date_arguments('20190101', '20181231')
        self.assertTrue(datefrom < dateto)

    def test_get_substantive_start_date(self):
        dl = ['20191001', '20191002', '20191003']
        self.assertEqual(TenseijingoDate.get_substantive_start_date('20190311', dl), '20191001')

    def test_get_substantive_end_date(self):
        dl = ['20191001', '20191002', '20191003']
        self.assertEqual(TenseijingoDate.get_substantive_end_date('20190311', dl), '20191003')


class TestTenseijingo(unittest.TestCase):
    @unittest.skip
    def test_get_html_with_date(self):
        from datetime import datetime as dt
        from os import listdir
        from os.path import isfile, join
        dtfrom = '20191215'
        dtto = '20190101'
        download_path = r'./html'
        tenseijingo.get_html_with_date(dtfrom, dtto, download_path)
        date_strings = ['{0}.{1}'.format(d.strftime('%Y%m%d'), 'html') for d in [dt.strptime('20190101', '%Y%m%d'), dt.strptime('20191215', '%Y%m%d')]]
        files_only = [f for f in listdir(download_path) if isfile(join(download_path, f))]


class TestTenseijingoModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = ini.User()
        cls.obj = TenseijingoModule(cls.user.id, cls.user.password)

    def test_init(self):
        self.assertEqual(self.obj.id, self.user.id)
        self.assertEqual(self.obj.password, self.user.password)

    def test_open_session(self):
        import requests
        s = self.obj.open_session()
        self.assertIsInstance(s, requests.Session)

    def test_get_contents_from_url(self):
        self.assertIsInstance(
            self.obj.get_contents_from_url('https://digital.asahi.com/articles/DA3S14049498.html'),
            bs
        )

    def test_get_contents_from_urls(self):
        results = self.obj.get_contents_from_urls(['https://digital.asahi.com/articles/DA3S14049498.html'])
        self.assertIsInstance(results, list)
        for res in results:
            self.assertIsInstance(res, bs)

    def test_convert_content_bs_to_dict(self):
        result_ok = self.obj.convert_content_bs_to_dict('https://digital.asahi.com/articles/DA3S14049498.html')
        # result_should_be_instance_of_dict
        self.assertIsInstance(result_ok, dict)
        # check element's type
        import datetime
        self.assertIsInstance(result_ok['title'], str)
        self.assertIsInstance(result_ok['content'], str)
        self.assertIsInstance(result_ok['datetime'], datetime.datetime)

    def test_get_backnumber_list(self):
        result = self.obj.get_backnumber_list()
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

    def test_convert_url(self):
        url = '/articles/DA3S14048182.html?iref=tenseijingo_backnumber'
        pattern = r'^http(s)?://digital\.asahi\.com/articles/(\d|\D)+\.html$'
        self.assertRegex(TenseijingoModule.convert_url(url), pattern)

    def test_making_html(self):
        content_result = self.obj.convert_content_bs_to_dict('https://digital.asahi.com/articles/DA3S14049498.html')
        result = TenseijingoModule.making_html(content_result)
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
