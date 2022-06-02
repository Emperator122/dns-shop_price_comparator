from selenium.webdriver.remote.webelement import WebElement


class Product:

    def __init__(self, name: str, price: float, url: str):
        self.name = name
        self.price = price
        self.url = url

    @staticmethod
    def from_web_element(a_element: WebElement, price_element: WebElement):
        price = float((price_element.text.split(' x ')[1].split('₽')[0]).replace(' ', ''))
        return Product(a_element.text, price, a_element.get_attribute('href'))

    @staticmethod
    def list_from_web_elements(a_elements: list, price_elements: list):
        assert len(a_elements) == len(price_elements)
        result = []
        for i in range(len(a_elements)):
            result.append(Product.from_web_element(a_elements[i], price_elements[i]))

        return result
