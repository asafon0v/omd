from omd_4 import Advert as OldAdvert


class ColorizeMixin:
    title: str
    price: int
    template: str

    repr_color_code = 32  # default color (green)

    def __repr__(self):
        return f"\033[1;{self.repr_color_code};40m" + self.template.format(title=self.title, price=self.price)


class Advert(ColorizeMixin, OldAdvert):
    repr_color_code = 35
    template = "{title} | {price} ₽"


if __name__ == '__main__':
    # test_1
    corgi = Advert({"title": "Вельш-корги", "category": "pets", "price": 1000})
    print(corgi)
