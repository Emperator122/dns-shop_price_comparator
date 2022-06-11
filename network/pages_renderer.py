from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from typing import Dict, Optional
from network.api.base_mainpage_cookies_loader import BaseMainPageCookiesLoader
from network.api.base import BaseRepository
import time


Cookies = Dict[str, str]


class PagesRenderer(BaseRepository, BaseMainPageCookiesLoader):
    driver: webdriver.Remote
    cookies: Cookies

    def __init__(self, user_agent: str, cookies: Cookies):
        super().__init__(user_agent=user_agent, cookies=cookies)
        chromedriver_autoinstaller.install()
        opts = Options()
        opts.add_argument(f"user-agent={user_agent}")
        opts.headless = True
        self.driver = webdriver.Chrome(options=opts)

    def get_cookies(self):  # override BaseMainPageCookiesLoader's method
        cookies = self.render_page('https://dns-shop.ru/')
        self.update_cookies(cookies)
        return

    def render_page(self, url, custom_cookies: Optional[Cookies] = None) -> Cookies:
        # load page
        self.driver.get(url)
        time.sleep(5)  # because of bug with selenium

        # add cookies
        if custom_cookies is not None:
            self.set_cookies(custom_cookies)
            self.driver.refresh()

        # get cookies
        cookies = self.driver.get_cookies()
        cookies_map = {}
        for cookie in cookies:
            cookies_map[cookie['name']] = cookie['value']

        # close browser
        self.driver.quit()

        return cookies_map

    def set_cookies(self, custom_cookies: Cookies):
        self.driver.delete_all_cookies()
        for cookie_name in custom_cookies:
            self.driver.add_cookie({
                'name': cookie_name,
                'value': custom_cookies[cookie_name]
            })
