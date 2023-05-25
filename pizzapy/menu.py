from typing import Dict, List, Optional, Any, Union, cast
from typing_extensions import TypedDict


from .urls import Urls, COUNTRY_USA
from .utils import request_json


class VariantInfo(TypedDict):
    Toppings: Dict[str, str]
    Tags: Dict[str, str]
    Code: str
    Name: str
    Price: str


class MenuCategory:
    def __init__(self, menu_data: Dict[str, Any] = {}, parent: Optional['MenuCategory'] = None) -> None:
        self.menu_data = menu_data
        self.subcategories: List['MenuCategory'] = []
        self.products: List['MenuItem'] = []
        self.parent = parent
        self.code = menu_data['Code']
        self.name = menu_data['Name']

    def get_category_path(self) -> str:
        path = '' if not self.parent else self.parent.get_category_path()
        return str(path + self.code)


class MenuItem:
    def __init__(self, data: Dict[str, Any] = {}) -> None:
        self.code = data['Code']
        self.name = data['Name']
        self.menu_data = data
        self.categories: List[MenuCategory] = []


class Menu:
    """The Menu is our primary interface with the API.

    This is far and away the most complicated class - it wraps up most of
    the logic that parses the information we get from the API.

    Next time I get pizza, there is a lot of work to be done in
    documenting this class.
    """
    def __init__(self, data: Dict[str, Any] = {}, country: str = COUNTRY_USA) -> None:
        self.variants: Dict[str, VariantInfo] = data.get('Variants', {})
        self.menu_by_code: Dict[str, MenuItem] = {}
        self.root_categories: Dict[str, MenuCategory] = {}
        self.country = COUNTRY_USA

        if self.variants:
            self.products = self.parse_items(data['Products'])
            self.coupons = self.parse_items(data['Coupons'])
            self.preconfigured = self.parse_items(data['PreconfiguredProducts'])
            for key, value in data['Categorization'].items():
                self.root_categories[key] = self.build_categories(value)

    @classmethod
    def from_store(cls, store_id: str, lang: str = 'en', country: str = COUNTRY_USA) -> 'Menu':
        response = request_json(Urls(country).menu_url(), store_id=store_id, lang=lang)
        menu = cls(response)
        return menu

    def build_categories(self, category_data: Dict[str, Any], parent: Optional[MenuCategory] = None) -> MenuCategory:
        category = MenuCategory(category_data, parent)
        for subcategory in category_data['Categories']:
            new_subcategory = self.build_categories(subcategory, category)
            category.subcategories.append(new_subcategory)
        for product_code in category_data['Products']:
            if product_code not in self.menu_by_code:
                #raise Exception('PRODUCT NOT FOUND: %s %s' % (product_code, category.code))
                continue
            product = self.menu_by_code[product_code]
            category.products.append(product)
            product.categories.append(category)
        return category

    def parse_items(self, parent_data: Dict[str, Any]) -> List[MenuItem]:
        items = []
        for code in parent_data.keys():
            obj = MenuItem(parent_data[code])
            self.menu_by_code[obj.code] = obj
            items.append(obj)
        return items

    def display(self) -> None:
        def print_category(category: MenuCategory, depth: int = 1) -> None:
            indent = "  " * (depth + 1)
            if len(category.products) + len(category.subcategories) > 0:
                print(indent + category.name)
                for subcategory in category.subcategories:
                    print_category(subcategory, depth + 1)
                for product in category.products:
                    print(indent + "  [%s]" % product.code, product.name)
        print("************ Coupon Menu ************")
        print_category(self.root_categories['Coupons'])
        print("************ Preconfigured Menu ************")
        print_category(self.root_categories['PreconfiguredProducts'])
        print("************ Regular Menu ************")
        print_category(self.root_categories['Food'])


    def search(self, name: str) -> None:
        for variant in self.variants.values():
            default_toppings = variant['Tags']['DefaultToppings'].split(',')
            variant['Toppings'] = {
                x.split('=', 1)[0]: x.split('=', 1)[1] for x in default_toppings if x
            }

            is_match = variant['Name'].find(name) != -1
            if is_match:
                print(f"{variant['Name']}\t{variant['Code']}\t{variant['Price']}")


    def get_item_count(self) -> int:
        return len(self.menu_by_code)
