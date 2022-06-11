from network.api.auth import AuthRepository
from network.api.orders import OrdersRepository
from network.api.products import ProductsRepository
from network.api.pages import PagesRepository
from models.produtct import OrdersGroup
from network.pages_renderer import PagesRenderer
import csv

if __name__ == "__main__":
    # input data
    USE_SELENIUM_FOR_INITIAL_COOKIES = False
    LOGIN = '******'
    PASSWORD = '*****'
    CSV_HEADER = ['url', 'name', 'status', 'delta']
    USER_AGENT = \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 ' \
        'Safari/537.36 '

    # session cookies
    cookies = {}

    # initialize repositories
    auth_repository = AuthRepository(USER_AGENT, cookies)
    orders_repository = OrdersRepository(USER_AGENT, cookies)
    products_repository = ProductsRepository(USER_AGENT, cookies)
    mainPageCookiesLoader = PagesRepository(USER_AGENT, cookies) if not USE_SELENIUM_FOR_INITIAL_COOKIES \
        else PagesRenderer(USER_AGENT, cookies)

    # get main page cookies
    print('Loading main page cookies...')
    mainPageCookiesLoader.get_cookies()

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
