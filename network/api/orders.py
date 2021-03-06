from typing import Dict
import requests
from urllib.parse import unquote
from network.api.base import BaseRepository
import re
from models.produtct import OrdersGroup, PaginatedOrdersGroups


class OrdersRepository(BaseRepository):

    def __init__(self, user_agent: str, cookies: Dict[str, str]):
        super().__init__(user_agent, cookies)

    def get_all_my_orders(self, update_cookies: bool = False) -> PaginatedOrdersGroups:
        # get orders groups
        orders_groups = {}
        i = 1
        while True:
            # get order groups for current page
            groups = self.get_my_orders(i, update_cookies)

            # we have no more orders
            if len(groups.keys()) == 0:
                break

            # groups from response
            for group_name in groups:
                group = groups[group_name]

                # if we have no dict for current group
                if not (group_name in orders_groups):
                    orders_groups[group_name] = []

                # add current group to list
                orders_groups[group_name].append(group)
            i += 1
        return orders_groups

    def get_my_orders(self, page: int, update_cookies: bool = False) -> Dict[str, OrdersGroup]:
        assert 'current_path' in self.cookies, 'current_path cookie is required'
        assert 'auth_access_token' in self.cookies, 'auth_access_token cookie is required'

        # extract city_id from current_path cookie
        current_path_string = unquote(self.cookies['current_path'])
        city_id = re.findall(r'\"city\":\"(.*?)\"', current_path_string)[0]

        # send request
        response = requests.get(
            f'https://restapi.dns-shop.ru/v1/profile-orders-get-list?page={page}&tab=all',
            cookies=self.cookies,
            headers={
                'accept': '*/*',
                'user-agent': self.user_agent,
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authaccesstoken': self.cookies['auth_access_token'],
                'cityid': city_id
            }
        )

        # extract json from response
        json = response.json()
        groups_json_dict = json['data']['groups']

        # we have no orders
        if groups_json_dict is None:
            if update_cookies:
                self.update_cookies(response.cookies)
            return {}

        # groups from response
        orders_groups = {}
        for group_name in groups_json_dict:
            group_json = groups_json_dict[group_name]
            # add current group to map
            orders_groups[group_name] = OrdersGroup.from_json(group_json)

        if update_cookies:
            self.update_cookies(response.cookies)
        return orders_groups
