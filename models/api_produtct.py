from typing import List, Dict
from uuid import UUID
from datetime import datetime

PaginatedOrdersGroups = Dict[str, List['APIOrdersGroup']]

class APIProduct:
    product_id: UUID
    code: int
    search_uid: str
    price: int
    count: int
    title: str
    url_img: str

    def __init__(self, id: UUID, code: int, search_uid: str, price: int, count: int, title: str, url_img: str) -> None:
        self.product_id = id
        self.code = code
        self.search_uid = search_uid
        self.price = price
        self.count = count
        self.title = title
        self.url_img = url_img

    def get_url(self):
        return f'https://www.dns-shop.ru/product/{self.search_uid}'

    @staticmethod
    def from_json(json: dict) -> 'APIProduct':
        return APIProduct(
            id=json['id'],
            code=json['code'],
            search_uid=json['searchUid'],
            price=json['price'],
            count=json['count'],
            title=json['title'],
            url_img=json['urlImg'],
        )


class APIOrder:
    id: UUID
    date: datetime
    price: int
    products: List[APIProduct]

    def __init__(self, order_id: UUID, date: datetime, price: int, products: List[APIProduct]) -> None:
        self.id = order_id
        self.type = type
        self.date = date
        self.price = price
        self.products = products

    @staticmethod
    def from_json(json: dict) -> 'APIOrder':
        products = []
        for item in json['products']:
            products.append(APIProduct.from_json(item))
        return APIOrder(
            order_id=json['id'],
            date=json['date'],
            price=json['price'],
            products=products,
        )


class APIOrdersGroup:
    orders: List[APIOrder]

    def __init__(self, orders: List[APIOrder]) -> None:
        self.orders = orders

    def get_products(self) -> List[APIProduct]:
        products = []
        for order in self.orders:
            for product in order.products:
                products.append(product)
        return products

    @staticmethod
    def get_products_from_paginated_groups(orders_groups: PaginatedOrdersGroups) -> List[APIProduct]:
        products = []
        for group_name in orders_groups:
            groups_pages = orders_groups[group_name]
            for group in groups_pages:
                products.extend(group.get_products())
        return products

    @staticmethod
    def from_json(json: list) -> 'APIOrdersGroup':
        orders = []
        for item in json:
            orders.append(APIOrder.from_json(item))
        return APIOrdersGroup(
            orders=orders,
        )
