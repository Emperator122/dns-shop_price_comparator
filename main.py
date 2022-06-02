from requests.utils import dict_from_cookiejar
import requests as reqs
from requests_toolbelt.multipart.encoder import MultipartEncoder
from selenium import webdriver
from urllib.parse import unquote
import re
import models.api_produtct as api_product
import models.api_microdata as api_microdata
import csv

driver = webdriver.Firefox()

driver.implicitly_wait(10)

# auth
driver.get('https://dns-shop.ru/')
user_agent = driver.execute_script("return navigator.userAgent;")

cookies = driver.get_cookies()
cookies_map = {}
for cookie in cookies:
    cookies_map[cookie['name']] = cookie['value']

m = MultipartEncoder({
    'LoginPasswordAuthorizationLoadForm[login]': '197012008@mail.ru',
    'LoginPasswordAuthorizationLoadForm[password]': 'a12181218',
    'LoginPasswordAuthorizationLoadForm[token]': '',
})

resp_0 = reqs.post(
        'https://www.dns-shop.ru/auth/auth/login-password-authorization/',
        data=m,
        cookies=cookies_map,
        headers={
            'accept': '*/*',
            'user-agent': user_agent,
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': m.content_type,
        }
    )

cookies = dict_from_cookiejar(resp_0.cookies)
for key in cookies:
    cookies_map[key] = cookies[key]

current_path_string = unquote(cookies_map['current_path'])
city_id = re.findall(r'\"city\":\"(.*?)\"', current_path_string)[0]

# get orders groups
orders_groups = {}
i = 1
while True:
    resp_1 = reqs.get(
        f'https://restapi.dns-shop.ru/v1/profile-orders-get-list?page={i}&tab=all',
        cookies=cookies_map,
        headers={
            'accept': '*/*',
            'user-agent': user_agent,
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authaccesstoken': cookies_map['auth_access_token'],
            'cityid': city_id
        }
    )
    resp1_json = resp_1.json()
    groups_json_dict = resp1_json['data']['groups']

    if groups_json_dict is None:
        break

    for group_name in groups_json_dict:
        group = groups_json_dict[group_name]

        if not (group_name in orders_groups):
            orders_groups[group_name] = []

        orders_groups[group_name].append(api_product.APIOrders.from_json(group))
    i += 1

# get actual prices
actual_products_microdata = {}
for group_name in orders_groups:
    groups_pages = orders_groups[group_name]
    for group in groups_pages:
        for order in group.orders:
            for product in order.products:
                resp_2 = reqs.get(
                    f'https://www.dns-shop.ru/product/microdata/{product.id}/',
                    cookies=cookies_map,
                    headers={
                        'accept': '*/*',
                        'user-agent': user_agent,
                        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    },
                )
                microdata = api_microdata.Microdata.from_json(resp_2.json())
                actual_products_microdata[str(product.id)] = microdata

# convert to csv
with open('delta.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    # header
    header = ['url', 'name', 'status', 'delta']
    writer.writerow(header)

    for group_name in orders_groups:
        groups_pages = orders_groups[group_name]
        for group in groups_pages:
            for order in group.orders:
                for product in order.products:
                    actual_product_microdata = actual_products_microdata[str(product.id)]
                    row = [
                        product.get_url(),
                        product.title,
                        actual_product_microdata.get_status(),
                        actual_product_microdata.get_price() - product.price
                        if actual_product_microdata.has_price()
                        else -1,
                    ]
                    writer.writerow(row)

print('Готово!')
