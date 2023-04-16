from typing import Optional
import json

from .address import Address


class Customer:
    """The Customer who orders a pizza."""

    def __init__(
        self,
        first_name: str = '',
        last_name: str = '',
        email: str = '',
        phone: str = '',
        address: Optional[str] = None,
    ) -> None:
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()
        self.str_address = address
        self.address = Address(*address.split(',')) if address else None

    def save(self, filename: str = "customers/customer1.json") -> None:
        """
        Saves the current customer to a .json file for loading later.
        """
        if not filename.startswith("customers"):
            filename = "customers/" + filename
        json_dict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.str_address,
        }

        with open(filename, "w") as f:
            json.dump(json_dict, f)

    @staticmethod
    def load(filename: str) -> 'Customer':
        """
        Load and return a new customer object from a json file.
        """
        with open(filename, "r") as f:
            data = json.load(f)

            customer = Customer(
                data["first_name"],
                data["last_name"],
                data["email"],
                data["phone"],
                data["address"],
            )
        return customer

    def __repr__(self) -> str:
        return (
            f"Name: {self.first_name} {self.last_name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Address: {self.address}"
        )
