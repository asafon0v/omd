import json
from keyword import iskeyword
from typing import Any, Dict


# task 1
class JsonChecker:
    def __init__(self, adv: Dict[str, Any]):
        adv_updated = {}
        for k, v in adv.items():
            if iskeyword(k) or not k.isidentifier():
                adv_updated.update({str(k) + "_": v})
            else:
                adv_updated.update({k: v})

        for k, v in adv_updated.items():
            if isinstance(v, dict):
                setattr(self, k, JsonChecker(v))
            else:
                setattr(self, k, v)


class Advert(JsonChecker):
    title: str
    price: int

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

    def __init__(self, obj: Dict[str, Any]):
        super().__init__(obj)

        if not hasattr(self, "title"):
            raise ValueError("the adv must have a title field")
        if not hasattr(self, "price"):
            self.price = 0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price: int):
        if price < 0:
            raise ValueError("price must be non-negative")

        self._price = price


if __name__ == '__main__':
    # test_1
    test_1_advert = """{
        "title": "python",
        "price": 10,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
            },
        "coolness": Infinity,
        "class": 11
        }"""

    advert_1 = Advert(json.loads(test_1_advert))

    print(advert_1)
    print(advert_1.location.address)
    print(advert_1.price)
    print(advert_1.coolness)

    # test_2
    test_2_advert = """{
            "def": 42,
            "class": 1,
            "title": "title",
            "Power": "alef-null"
            }"""

    advert_2 = Advert(json.loads(test_2_advert))

    print(advert_2)
    print(advert_2.price)
    print(advert_2.def_)
    print(advert_2.class_)
    print(advert_2.Power)
