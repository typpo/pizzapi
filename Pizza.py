from pizzapy import Customer, StoreLocator

customer = Customer("Stephen", "Monroe", "sdmonroe1999@gmail.com", "980-255-9893",
                    "705 17th Street, Knoxville, TN, 37916")

my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print(my_local_dominos)
print("\nMENU\n")

menu = my_local_dominos.get_menu()


def searchMenu(menu):
    print("You are now searching the menu...")
    while True:
        item = input("Type an item to look for: ").strip().lower

        if item != "" and len(item) > 0:
            item = item[0].upper + item[1:]
        else:
            print("Invalid, exiting search...")
            break

        print(f"Results for: {item}")
        menu.search(Name=item)


searchMenu(menu)
