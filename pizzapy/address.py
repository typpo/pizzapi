from typing import List, Union, Dict
from .store import Store
from .utils import request_json
from .urls import Urls, COUNTRY_USA

class Address:
    """Create an address, for finding stores and placing orders.

    The Address object describes a street address in North America (USA or
    Canada, for now). Callers can use the Address object's methods to find
    the closest or nearby stores from the API.

    Attributes:
        street (str): Street address
        city (str): North American city
        region (str): North American region (state, province, territory)
        zip (str): North American ZIP code
        urls (Urls): Country-specific URLs
        country (str): Country
    """

    def __init__(self, street: str, city: str, region: str = '', zip: Union[str, int] = '', country: str = COUNTRY_USA) -> None:
        self.street: str = street.strip()
        self.city: str = city.strip()
        self.region: str = region.strip()
        self.zip: str = str(zip).strip()
        self.urls: Urls = Urls(country)
        self.country: str = country

    def __repr__(self) -> str:
        return ", ".join([self.street, self.city, self.region, self.zip])

    @property
    def data(self) -> Dict[str, str]:
        return {'Street': self.street, 'City': self.city,
                'Region': self.region, 'PostalCode': self.zip}

    @property
    def line1(self) -> str:
        return '{Street}'.format(**self.data)

    @property
    def line2(self) -> str:
        return '{City}, {Region}, {PostalCode}'.format(**self.data)

    def nearby_stores(self, service: str = 'Delivery') -> List[Store]:
        """Query the API to find nearby stores.

        nearby_stores will filter the information we receive from the API
        to exclude stores that are not currently online (!['IsOnlineNow']),
        and stores that are not currently in service (!['ServiceIsOpen']).
        """
        data = request_json(self.urls.find_url(), line1=self.line1, line2=self.line2, type=service)
        return [Store(x, self.country) for x in data['Stores']
                if x['IsDeliveryStore'] and x['IsOnlineNow'] and x['ServiceIsOpen'][service]] \
            if service == 'Delivery' else \
            [Store(x, self.country) for x in data['Stores']
             if x['IsOnlineNow'] and x['ServiceIsOpen'][service]]

    def closest_store(self, service: str = 'Delivery') -> Store:
        stores = self.nearby_stores(service=service)
        if not stores:
            raise Exception('No local stores are currently open')
        return stores[0]
