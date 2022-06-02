from requests.utils import dict_from_cookiejar
from api.auth import AuthRepository
from api.orders import OrdersRepository
from api.products import ProductsRepository
import requests as reqs
from requests_toolbelt.multipart.encoder import MultipartEncoder
from selenium import webdriver
from urllib.parse import unquote
import re
from models.api_produtct import APIOrdersGroup
import models.api_microdata as api_microdata
import csv

LOGIN = '197012008@mail.ru'
PASSWORD = 'a12181218'
CSV_HEADER = ['url', 'name', 'status', 'delta']

driver = webdriver.Firefox()

# auth
driver.get('https://dns-shop.ru/')
user_agent = driver.execute_script("return navigator.userAgent;")

cookies = driver.get_cookies()
cookies_map = {}
for cookie in cookies:
    cookies_map[cookie['name']] = cookie['value']

# initialize repositories
auth_repository = AuthRepository(user_agent, cookies_map)
orders_repository = OrdersRepository(user_agent, cookies_map)
products_repository = ProductsRepository(user_agent, cookies_map)

# login
auth_repository.login(LOGIN, PASSWORD)

# get user's orders
orders_groups = orders_repository.get_all_my_orders()
products = APIOrdersGroup.get_products_from_paginated_groups(orders_groups)

# get actual prices
actual_products_microdata = products_repository.get_microdata_from_products_groups(products)

# save to csv
with open('delta.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    # insert header
    writer.writerow(CSV_HEADER)

    for product in products:
        actual_product_microdata = actual_products_microdata[str(product.product_id)]
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
