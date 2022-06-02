from requests.utils import dict_from_cookiejar
import requests as reqs
from requests_toolbelt.multipart.encoder import MultipartEncoder
import http.client
from http.cookies import SimpleCookie
import selenium.webdriver.common.by as by
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from models.product import Product
import time
import csv

driver = webdriver.Firefox()

http.client._MAXHEADERS = 1000
driver.implicitly_wait(10)

# auth
driver.get('https://dns-shop.ru/')

profile_div = driver.find_element(by=by.By.XPATH, value="//div[contains(@class, 'user-profile__login')]")
hover = ActionChains(driver).move_to_element(profile_div)
hover.perform()
time.sleep(2)

driver.find_element(by=by.By.XPATH, value="//button[contains(@class, 'user-menu__button')]").click()
driver.find_element(by=by.By.XPATH, value="//div[contains(@class, 'block-other-login-methods__password-caption')]") \
    .click()
driver.find_element(by=by.By.XPATH, value="//input[contains(@autocomplete, 'username')]") \
    .send_keys('197012008@mail.ru')
driver.find_element(by=by.By.XPATH, value="//input[contains(@autocomplete, 'current-password')]") \
    .send_keys('a12181218')
driver.find_element(by=by.By.XPATH, value="//div[contains(@class, 'form-entry-with-password__main-button')]") \
    .click()

# go to profile
driver.get('https://www.dns-shop.ru/profile/order/all/')

# load orders
while True:
    time.sleep(1)

    next_buttons = driver.find_elements(by=by.By.XPATH,
                                        value="//div[contains(@class, 'order-list-pagination__show-more')]")
    if len(next_buttons) == 0:
        break
    next_buttons[0].click()

driver.implicitly_wait(1)

# open spoilers
flipped_elements = driver.find_elements(by=by.By.XPATH,
                                        value="//img[contains(@class, 'order-header__hide-button-image_flipped')]")
driver.implicitly_wait(10)

for element in flipped_elements:
    element.click()

# load products
products_a = driver.find_elements(by=by.By.XPATH, value="//a[contains(@class, 'order-product__name')]")
products_prices = driver.find_elements(by=by.By.XPATH,
                                       value="//div[contains(@class, 'order-price-block__sub-info')]")
time.sleep(1)
old_products = Product.list_from_web_elements(products_a, products_prices)

# load new prices
new_products = []
delta_products = []
for product in old_products:
    if product.url is None:
        continue
    driver.get(product.url)
    product_price_element = driver.find_element(
            by=by.By.XPATH,
            value="//div[contains(@class, 'product-buy__price-wrap')]")
    time.sleep(2)
    # try to get price
    split_price = product_price_element.text.split('₽')
    product_price = -1
    if len(split_price) >= 1:
        try:
            product_price = float(split_price[0].replace(' ', ''))
        except ValueError:
            pass
    new_products.append(Product(product.name, product_price, product.url))
    delta_products.append(Product(product.name, product_price if product_price == -1 else product_price-product.price,
                                  product.url))

# convert to csv
with open('delta.csv', 'w') as f:
    writer = csv.writer(f)

    # header
    header = ['url', 'name', 'delta']
    writer.writerow(header)

    for product in delta_products:
        writer.writerow([product.url, product.name, product.price])

print('lala')
