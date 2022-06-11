from abc import ABC


class BaseMainPageCookiesLoader(ABC):
    def get_cookies(self):
        pass
