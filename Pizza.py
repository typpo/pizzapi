from pizzapy import Customer, StoreLocator, Order, ConsoleInput


def searchMenu(menu):
    print("You are now searching the menu...")

    item = input("Type an item to look for: ").strip().lower

    if len(item) > 0:
        item = item[0].upper + item[1:]
        print(f"Results for: {item}")
        menu.search(Name=item)
        print()
    else:
        print("No Results")


def addToOrder(order):
    print("Please type the codes of the items you'd like to order...")
    print("Press ENTER to stop ordering.")
    while True:
        item = input("Code: ").upper()
        try:
            order.add_item(item)
        except:
            if item == "":
                break
            print("Invalid Code...")


customer = ConsoleInput.get_new_customer()

my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print(my_local_dominos)
print("\nMENU\n")

menu = my_local_dominos.get_menu()
order = Order.begin_customer_order(customer, my_local_dominos, "us")

while True:
    searchMenu(menu)
    addToOrder(order)
    answer = input("Would you like to add more items (y/n)?")
    if answer.lower() not in ["yes", "y"]:
        break

total = 0
print("\nYour order is as follows: ")
for item in order.data["Products"]:
    price = item["price"]
    print(item["Name"] + " $" + item["Price"])
    total += float(price)

print("\nYour order total is: $" + str(total) + " TAX")

card = ConsoleInput.get_credit_card()
