from network.api.auth import AuthRepository
from network.api.orders import OrdersRepository
from network.api.products import ProductsRepository
from network.pages_renderer import PagesRenderer
from models.produtct import OrdersGroup
import csv

# input data
LOGIN = '***'
PASSWORD = '****'
CSV_HEADER = ['url', 'name', 'status', 'delta']

# make first main page render for getting cookies
page_renderer = PagesRenderer()
render_result = page_renderer.render_page('https://dns-shop.ru/')
user_agent = render_result.user_agent
cookies = render_result.cookies

# initialize repositories
auth_repository = AuthRepository(user_agent, cookies)
orders_repository = OrdersRepository(user_agent, cookies)
products_repository = ProductsRepository(user_agent, cookies)

# login
print('Logining in...')
auth_repository.login(LOGIN, PASSWORD)

# get user's orders
print('Loading user\'s orders...')
orders_groups = orders_repository.get_all_my_orders()
products = OrdersGroup.get_products_from_paginated_groups(orders_groups)

# get actual prices
print('Loading actual prices...')
actual_products_microdata = products_repository.get_microdata_from_products_groups(products)

# save to csv
print('Saving...')
with open('delta.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    # insert header
    writer.writerow(CSV_HEADER)

    # insert products info
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
print('Saved!')
