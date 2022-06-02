from selenium import webdriver
from typing import Dict, Optional


Cookies = Dict[str, str]


class PagesRenderer:

    @staticmethod
    def render_page(url, custom_cookies: Optional[Cookies] = None) -> 'PageRenderResult':
        # load page
        driver = webdriver.Firefox()
        driver.get(url)

        # add cookies
        if custom_cookies is not None:
            PagesRenderer.set_cookies(driver, custom_cookies)
            driver.refresh()

        # get ua
        user_agent = driver.execute_script("return navigator.userAgent;")

        # get cookies
        cookies = driver.get_cookies()
        cookies_map = {}
        for cookie in cookies:
            cookies_map[cookie['name']] = cookie['value']

        # close browser
        driver.close()

        return PageRenderResult(cookies_map, user_agent)

    @staticmethod
    def set_cookies(driver: webdriver.Remote, custom_cookies: Cookies):
        driver.delete_all_cookies()
        for cookie_name in custom_cookies:
            driver.add_cookie({
                'name': cookie_name,
                'value': custom_cookies[cookie_name]
            })




class PageRenderResult:
    cookies: Cookies
    user_agent: str

    def __init__(self, cookies: Cookies, user_agent: str):
        self.cookies = cookies
        self.user_agent = user_agent
