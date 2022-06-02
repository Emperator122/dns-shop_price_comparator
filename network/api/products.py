from typing import Dict, List
import requests
from uuid import UUID
from models.microdata import Microdata
from models.produtct import Product
from network.api.base import BaseRepository


class ProductsRepository(BaseRepository):
    user_agent: str
    cookies: Dict[str, str]

    def __init__(self, user_agent: str, cookies: Dict[str, str]):
        super().__init__(user_agent, cookies)

    def get_microdata_from_products_groups(self, products: List[Product],
                                           update_cookies: bool = False):
        products_microdata = {}
        for product in products:
            # get product microdata and save it
            microdata = self.get_microdata(product.product_id, update_cookies)
            products_microdata[str(product.product_id)] = microdata

        return products_microdata

    def get_microdata(self, product_uuid: UUID, update_cookies: bool = False) -> Microdata:
        response = requests.get(
                    f'https://www.dns-shop.ru/product/microdata/{product_uuid}/',
                    cookies=self.cookies,
                    headers={
                        'accept': '*/*',
                        'user-agent': self.user_agent,
                        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    },
                )
        # extract json from response
        json = response.json()
        microdata = Microdata.from_json(json)

        if update_cookies:
            self.update_cookies(response.cookies)

        return microdata
