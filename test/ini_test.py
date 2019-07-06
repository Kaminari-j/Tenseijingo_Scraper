import unittest
from tenseijingo.ini import User, TelegramBot


class Test_User(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.userinfo = User()

    def test_init(self):
        self.assertTrue(self.userinfo.init_status)

    def test_load_env(self):
        self.assertIsNotNone(self.userinfo.id)
        self.assertIsNotNone(self.userinfo.password)


if __name__ == '__main__':
    unittest.main()


class Test_TelegramBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = TelegramBot()

    def test_init(self):
        self.assertTrue(self.bot.init_status)

    def test_load_env(self):
        self.assertIsNotNone(self.bot.token)


if __name__ == '__main__':
    unittest.main()
