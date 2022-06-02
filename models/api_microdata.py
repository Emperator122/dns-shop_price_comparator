from typing import List


class Offers:
    offer_type: str
    url: str
    availability: str
    price: int
    price_currency: str

    def __init__(self, offer_type: str, url: str, availability: str, price: int, price_currency: str) -> None:
        self.offer_type = offer_type
        self.url = url
        self.availability = availability
        self.price = price
        self.price_currency = price_currency

    @staticmethod
    def from_json(json: dict) -> 'Offers':
        return Offers(
            offer_type=json['@type'],
            url=json['url'],
            availability=json['availability'],
            price=json['price'],
            price_currency=json['priceCurrency'],
        )

    @staticmethod
    def empty() -> 'Offers':
        return Offers(
            offer_type='',
            url='',
            availability='',
            price=-1,
            price_currency='',
        )


class Data:
    context: str
    data_type: str
    name: str
    description: str
    sku: int
    offers: Offers
    image: List[str]

    def __init__(self, context: str, data_type: str, name: str, description: str, sku: int, offers: Offers,
                 image: List[str]) -> None:
        self.context = context
        self.data_type = data_type
        self.name = name
        self.description = description
        self.sku = sku
        self.offers = offers
        self.image = image

    @staticmethod
    def from_json(json: dict) -> 'Data':
        images = []
        if 'image' in json:
            for image in json['image']:
                images.append(image)

        offers = Offers.empty()
        if 'offers' in json:
            offers = Offers.from_json(json['offers'])

        return Data(
            context=json['@context'],
            data_type=json['@type'],
            name=json['name'],
            description=json['description'],
            sku=json['sku'],
            offers=offers,
            image=json['image'],
        )

    @staticmethod
    def empty() -> 'Data':
        return Data(
            context='',
            data_type='',
            name='',
            description='',
            sku=-1,
            offers=Offers.empty(),
            image=[],
        )


class Microdata:
    result: bool
    data: Data
    message: str

    def __init__(self, result: bool, data: Data, message: str) -> None:
        self.result = result
        self.data = data
        self.message = message

    def has_price(self) -> bool:
        return self.result and self.data.offers.price != -1

    def get_price(self):
        return self.data.offers.price

    def get_status(self):
        value = 'Не известно'
        if self.data.offers.availability == 'https://schema.org/InStock':
            value = 'В наличии'
        elif self.data.offers.availability == 'https://schema.org/OutOfStock':
            value = 'Нет в наличии'
        return value


    @staticmethod
    def from_json(json: dict) -> 'Microdata':
        return Microdata(
            result=json["result"],
            data=Data.from_json(json['data']),
            message=json["message"]
        ) if json["result"] is True else Microdata(False, Data.empty(), '')
