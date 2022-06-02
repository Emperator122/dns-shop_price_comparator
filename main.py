from requests.utils import dict_from_cookiejar
from requests_html import HTMLSession
import requests as reqs
from requests_toolbelt.multipart.encoder import MultipartEncoder
import http.client
from http.cookies import SimpleCookie
import selenium


http.client._MAXHEADERS = 1000

session = HTMLSession()

script = """
    () => {
        
        return document.cookie;
    }
"""

req_1 = session.get('https://club.dns-shop.ru/review/',
                    headers={
                        'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
                        'Connection': 'keep-alive',
                      'Accept-Language': 'en-us,en;q=0.5',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    },
                    )

page_cookies_list = req_1.html.render(sleep=5, script=script)
cookie = SimpleCookie()
cookie.load(page_cookies_list)
page_cookies_map = {k: v.value for k, v in cookie.items()}
page_cookies_map.update(dict_from_cookiejar(req_1.cookies))


req_2 = session.get('https://club.dns-shop.ru/review/',
                    headers={
                        'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    },
                    cookies=page_cookies_map
                    )
page_cookies_list2 = req_2.html.render(sleep=5, script=script)
cookie = SimpleCookie()
cookie.load(page_cookies_list2)
page_cookies_map2 = {k: v.value for k, v in cookie.items()}
page_cookies_map2.update(dict_from_cookiejar(req_2.cookies))
# csrf = req_2.html.find('meta[name="csrf-token"]')[0].attrs['content']
# page_cookies_map2['_csrf'] = req_2.html.find('meta[name="csrf-token"]')[0].attrs['content']
# page_cookies_map.update(dict_from_cookiejar(req_1.cookies))
#
# req_3 = session.get('https://www.dns-shop.ru/auth/auth/login-password-authorization/',
#                     headers={
#                         'Accept': '*/*',
#                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
#                         'Accept-Language': 'en-us,en;q=0.5',
#                         'Accept-Encoding': 'gzip, deflate',
#                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#                     },
#                     cookies=page_cookies_map
#                     )
# page_cookies_list3 = req_3.html.render(sleep=5, script=script)
# cookie = SimpleCookie()
# cookie.load(page_cookies_list3)
# page_cookies_map3 = {k: v.value for k, v in cookie.items()}
# page_cookies_map3.update(dict_from_cookiejar(req_3.cookies))





mp_encoder = MultipartEncoder(
    fields={
        'LoginPasswordAuthorizationLoadForm[login]': '1998120088@gmail.com',
        'LoginPasswordAuthorizationLoadForm[password]': 'a12181218',
        'LoginPasswordAuthorizationLoadForm[token]': '',
        # 'login': '1998120088@mail.com',
        # 'password': 'a12181218',
        # 'token': '',
    }
)
response = reqs.post('https://www.dns-shop.ru/auth/auth/login-password-authorization/',
                         data=mp_encoder,
                         headers={'Content-Type': mp_encoder.content_type,
                                  'Accept': '*/*',
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
                                  },
                        cookies=page_cookies_map2
                        )
print('lala')
