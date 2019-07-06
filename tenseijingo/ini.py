import os
from os.path import join, dirname
from dotenv import load_dotenv


# Todo : need test script
class User:
    init_status = bool
    __USER_ID = None
    __USER_PASSWORD = None

    def __init__(self):
        self.load_env('../ini/user.ini')
        if self.__USER_ID and self.__USER_PASSWORD:
            self.init_status = True
        else:
            self.init_status = False

    # 環境変数ロード
    def load_env(self, ini_path=None):
        # 環境変数設定
        env_path = join(dirname(__file__), ini_path)
        load_dotenv(env_path)
        self.__USER_ID = os.environ.get("_USER_ID")
        self.__USER_PASSWORD = os.environ.get("_USER_PASSWORD")

    @property
    def id(self):
        return self.__USER_ID

    @property
    def password(self):
        return self.__USER_PASSWORD


class TelegramBot:
    init_status = bool
    __TOKEN = None

    def __init__(self):
        self.load_env('../ini/tele.ini')
        if self.__TOKEN:
            self.init_status = True
        else:
            self.init_status = False

    # 環境変数ロード
    def load_env(self, ini_path=None):
        # 環境変数設定
        env_path = join(dirname(__file__), ini_path)
        load_dotenv(env_path)
        self.__TOKEN = os.environ.get("_TOKEN")

    @property
    def token(self):
        return self.__TOKEN
