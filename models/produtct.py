from typing import List, Dict
from uuid import UUID
from datetime import datetime

PaginatedOrdersGroups = Dict[str, List['APIOrdersGroup']]


class Product:
    product_id: UUID
    code: int
    search_uid: str
    price: int
    count: int
    title: str
    url_img: str

    def __init__(self, product_id: UUID, code: int, search_uid: str, price: int, count: int, title: str, url_img: str) \
            -> None:
        self.product_id = product_id
        self.code = code
        self.search_uid = search_uid
        self.price = price
        self.count = count
        self.title = title
        self.url_img = url_img

    def get_url(self):
        return f'https://www.dns-shop.ru/product/{self.search_uid}'

    @staticmethod
    def from_json(json: dict) -> 'Product':
        return Product(
            product_id=json['id'],
            code=json['code'],
            search_uid=json['searchUid'],
            price=json['price'],
            count=json['count'],
            title=json['title'],
            url_img=json['urlImg'],
        )


class Order:
    id: UUID
    date: datetime
    price: int
    products: List[Product]

    def __init__(self, order_id: UUID, date: datetime, price: int, products: List[Product]) -> None:
        self.id = order_id
        self.type = type
        self.date = date
        self.price = price
        self.products = products

    @staticmethod
    def from_json(json: dict) -> 'Order':
        products = []
        for item in json['products']:
            products.append(Product.from_json(item))
        return Order(
            order_id=json['id'],
            date=json['date'],
            price=json['price'],
            products=products,
        )


class OrdersGroup:
    orders: List[Order]

    def __init__(self, orders: List[Order]) -> None:
        self.orders = orders

    def get_products(self) -> List[Product]:
        products = []
        for order in self.orders:
            for product in order.products:
                products.append(product)
        return products

    @staticmethod
    def get_products_from_paginated_groups(orders_groups: PaginatedOrdersGroups) -> List[Product]:
        products = []
        for group_name in orders_groups:
            groups_pages = orders_groups[group_name]
            for group in groups_pages:
                products.extend(group.get_products())
        return products

    @staticmethod
    def from_json(json: list) -> 'OrdersGroup':
        orders = []
        for item in json:
            orders.append(Order.from_json(item))
        return OrdersGroup(
            orders=orders,
        )
