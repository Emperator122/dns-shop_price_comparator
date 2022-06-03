from typing import Dict, Optional
from network.api.base import BaseRepository
import re
from http.cookies import SimpleCookie
import dukpy
import requests
import http.client

IPP_JS_PATH = 'resources/ipp_full.js'


class PagesRepository(BaseRepository):
    def __init__(self, user_agent: str, cookies: Dict[str, str] = None):
        super().__init__(user_agent, cookies)

    def get_main_page_cookies(self):
        # first we get ipp cookies
        self.get_ipp_cookies()
        # then we load main page with ipp cookies
        # and get more cookies
        self.load_main_page()

    def get_ipp_cookies(self):
        # send request to main page
        response = self.load_main_page(False)
        # get js for tokens generation
        js_code_regex_result = \
            re.findall(r'<script type=\"text/javascript\">(.*)</script>', response.text, flags=re.S | re.M)
        assert len(js_code_regex_result) > 0
        js_code = js_code_regex_result[0]

        # edit js to extract cookies from script's result
        with open(IPP_JS_PATH, encoding='utf8') as f:
            part_of_code = f.read()
        js_code = part_of_code + '\r\n' + js_code + '\r\n' + 'document.cookie'

        # evaluate js
        ipp_cookies_string = dukpy.evaljs(js_code, user_agent=self.user_agent)

        # update cookies
        ipp_cookies = SimpleCookie()
        ipp_cookies.load(ipp_cookies_string)
        for k, v in ipp_cookies.items():
            self.cookies[k] = v.value

    def load_main_page(self, update_cookies=True) -> requests.Response:
        http.client._MAXHEADERS = 1000
        # send request to main page
        response = requests.get(
            'https://dns-shop.ru/',
            headers={
                'accept': '*/*',
                'user-agent': self.user_agent,
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            },
            cookies=self.cookies,
        )

        if update_cookies:
            self.update_cookies(response.cookies)

        return response
