from pizzapy import Customer, StoreLocator

customer = Customer("Stephen", "Monroe", "sdmonroe1999@gmail.com", "980-255-9893",
                    "705 17th Street, Knoxville, TN, 37916")

my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print(my_local_dominos)
