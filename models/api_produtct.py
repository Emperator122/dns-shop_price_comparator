from typing import List
from uuid import UUID
from datetime import datetime


class APIProduct:
    id: UUID
    code: int
    search_uid: str
    price: int
    count: int
    title: str
    url_img: str

    def __init__(self, id: UUID, code: int, search_uid: str, price: int, count: int, title: str, url_img: str) -> None:
        self.id = id
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

    def __init__(self, id: UUID, date: datetime, price: int, products: List[APIProduct]) -> None:
        self.id = id
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
            id=json['id'],
            date=json['date'],
            price=json['price'],
            products=products,
        )


class APIOrders:
    orders: List[APIOrder]

    def __init__(self, orders: List[APIOrder]) -> None:
        self.orders = orders

    @staticmethod
    def from_json(json: list) -> 'APIOrders':
        orders = []
        for item in json:
            orders.append(APIOrder.from_json(item))
        return APIOrders(
            orders=orders,
        )
