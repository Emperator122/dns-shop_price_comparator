from typing import Dict
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from network.api.base import BaseRepository


class AuthRepository(BaseRepository):
    user_agent: str
    cookies: Dict[str, str]

    def __init__(self, user_agent: str, cookies: Dict[str, str]):
        super().__init__(user_agent, cookies)

    def login(self, username: str, password: str, update_cookies=True):
        m = MultipartEncoder({
            'LoginPasswordAuthorizationLoadForm[login]': username,
            'LoginPasswordAuthorizationLoadForm[password]': password,
            'LoginPasswordAuthorizationLoadForm[token]': '',
        })
        response = requests.post(
            'https://www.dns-shop.ru/auth/auth/login-password-authorization/',
            data=m,
            cookies=self.cookies,
            headers={
                'accept': '*/*',
                'user-agent': self.user_agent,
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Content-Type': m.content_type,
            }
        )

        if update_cookies:
            self.update_cookies(response.cookies)
