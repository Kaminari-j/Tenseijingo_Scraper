import unittest
from tenseijingoscraper import downloader


class TestTenseijingo(unittest.TestCase):
    @unittest.skip
    def test_get_html_with_date(self):
        from datetime import datetime as dt
        from os import listdir
        from os.path import isfile, join
        date_from = '20191215'
        date_to = '20190101'
        download_path = r'./html'
        downloader.get_html_with_date(date_from, date_to, download_path)
        date_strings = ['{0}.{1}'.format(d.strftime('%Y%m%d'), 'html') for d in [dt.strptime('20190101', '%Y%m%d'), dt.strptime('20191215', '%Y%m%d')]]
        files_only = [f for f in listdir(download_path) if isfile(join(download_path, f))]


if __name__ == '__main__':
    unittest.main()
