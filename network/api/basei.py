from abc import ABC
from typing import Dict
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar


class BaseRepository(ABC):
    user_agent: str
    cookies: Dict[str, str]

    def __init__(self, user_agent: str, cookies: Dict[str, str]):
        self.user_agent = user_agent
        self.cookies = cookies

    def update_cookies(self, cookies: RequestsCookieJar):
        cookies = dict_from_cookiejar(cookies)
        for key in cookies:
            self.cookies[key] = cookies[key]
