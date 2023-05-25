from pizzapy import Customer, StoreLocator, Order, ConsoleInput, Address


def searchMenu(menu):
    print("You are now searching the menu...")
    print(f'Number of items: {menu.get_item_count()}')
    menu.display()

    item = input("Type an item to look for: ").strip().lower()

    if len(item) > 0:
        item = item[0].upper() + item[1:]
        print(f"Results for: {item}\n")
        menu.search(name=item)
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


#customer = ConsoleInput.get_new_customer()
address = Address('444 de haro st', 'San Francisco', 'CA', '94107')
customer = Customer('Ian', 'Web', 'web@example.com', '123-456-7890', address)

my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
print("\nClosest Store:")
print(my_local_dominos)

#ans = input("Would you like to order from this store? [y/N]")
#if ans.lower() not in ["yes", "y"]:
#    print("Goodbye!")
#    quit()

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
    print('Item:', item)
    price = item["Price"]
    print(item["Name"] + " $" + item["Price"])
    total += float(price)

print("\nYour order total is: $" + str(total) + " TAX")

payment = input("\nWill you be paying with CASH or CREDIT CARD? (CASH, CREDIT CARD)")
if payment.lower() in ["card", "credit card"]:
    card = ConsoleInput.get_credit_card()
else:
    card = False

ans = input("\nWould you like to place this order? (y/n)")
if ans.lower in ["y", "yes"]:
    order.place(card)
    my_local_dominos.place_order(order, card)
    print("Order Placed!")
else:
    print("Goodbye!")
