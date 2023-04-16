import requests
from typing import List, Dict, Any, Optional
from .menu import Menu
from .urls import Urls, COUNTRY_USA
from .customer import Customer
from .store import Store
from .address import Address
from .payment import CreditCard


class Order:
    def __init__(self, store: Store, customer: Customer, country: str = COUNTRY_USA) -> None:
        self.store = store
        self.menu = Menu.from_store(store_id=store.id, country=country)
        self.customer = customer
        self.address = customer.address
        self.urls = Urls(country)
        self.data: Dict[str, Any] = {
            'Address': {'Street': self.address.street,
                        'City': self.address.city,
                        'Region': self.address.region,
                        'PostalCode': self.address.zip,
                        'Type': 'House'},
            'Coupons': [], 'CustomerID': '', 'Extension': '',
            'OrderChannel': 'OLO', 'OrderID': '', 'NoCombine': True,
            'OrderMethod': 'Web', 'OrderTaker': None, 'Payments': [],
            'Products': [], 'Market': '', 'Currency': '',
            'ServiceMethod': 'Delivery', 'Tags': {}, 'Version': '1.0',
            'SourceOrganizationURI': 'order.dominos.com', 'LanguageCode': 'en',
            'Partners': {}, 'NewUser': True, 'metaData': {}, 'Amounts': {},
            'BusinessDate': '', 'EstimatedWaitMinutes': '',
            'PriceOrderTime': '', 'AmountsBreakdown': {}
        }

    @staticmethod
    def begin_customer_order(customer: Customer, store: Store, country: str = COUNTRY_USA) -> 'Order':
        return Order(store, customer, country=country)

    def __repr__(self) -> str:
        return f"An order for {self.customer.first_name} with {len(self.data['Products']) if self.data['Products'] else 'no'} items in it"

    def add_item(self, code: str, qty: int = 1, options: List[str] = []) -> Dict[str, Any]:
        item = self.menu.variants[code]
        item.update(ID=1, isNew=True, Qty=qty, AutoRemove=False)
        print('appending', item)
        self.data['Products'].append(item)
        return item

    def remove_item(self, code: str) -> Dict[str, Any]:
        codes = [x['Code'] for x in self.data['Products']]
        return self.data['Products'].pop(codes.index(code))

    def add_coupon(self, code: str, qty: int = 1) -> Dict[str, Any]:
        item = self.menu.variants[code]
        item.update(ID=1, isNew=True, Qty=qty, AutoRemove=False)
        self.data['Coupons'].append(item)
        return item

    def remove_coupon(self, code: str) -> Dict[str, Any]:
        codes = [x['Code'] for x in self.data['Coupons']]
        return self.data['Coupons'].pop(codes.index(code))

    def changeToCarryout(self) -> None:
        self.data['ServiceMethod'] = 'Carryout'

    def changeToDelivery(self) -> None:
        self.data['ServiceMethod'] = 'Delivery'

    def _send(self, url: str, merge: bool) -> Dict[str, Any]:
        self.data.update(
            StoreID=self.store.id,
            Email=self.customer.email,
            FirstName=self.customer.first_name,
            LastName=self.customer.last_name,
            Phone=self.customer.phone,
        )

        for key in ('Products', 'StoreID', 'Address'):
            if key not in self.data or not self.data[key]:
                raise Exception(f'order has invalid value for key "{key}"')

        headers = {
            'Referer': 'https://order.dominos.com/en/pages/order/',
            'Content-Type': 'application/json'
        }

        r = requests.post(url=url, headers=headers, json={'Order': self.data})
        r.raise_for_status()
        json_data = r.json()

        if merge:
            for key, value in json_data['Order'].items():
                if value or not isinstance(value, list):
                    self.data[key] = value
        return json_data #type: ignore

    def validate(self) -> bool:
        response = self._send(self.urls.validate_url(), True)
        return bool(response['Status'] != -1)

    def place(self, card: Optional[CreditCard]) -> Dict[str, Any]:
        self.pay_with(card)
        response = self._send(self.urls.place_url(), False)
        return response

    def pay_with(self, card: Optional[CreditCard]) -> Dict[str, Any]:
        response = self._send(self.urls.price_url(), True)

        if response['Status'] == -1:
            raise Exception(f'get price failed: {response}')

        if not card:
            self.data['Payments'] = [
                {
                    'Type': 'Cash',
                }
            ]
        else:
            self.data['Payments'] = [
                {
                    'Type': 'CreditCard',
                    'Expiration': card.expiration,
                    'Amount': self.data['Amounts'].get('Customer', 0),
                    'CardType': card.card_type,
                    'Number': int(card.number),
                    'SecurityCode': int(card.cvv),
                    'PostalCode': int(card.zip)
                }
            ]

        return response
