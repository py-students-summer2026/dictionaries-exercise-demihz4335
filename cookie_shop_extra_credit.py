"""
Extra credit version of the virtual cookie shop.
Run this file through a main file in the same way as cookie_shop.py.
"""

import csv


def bake_cookies(filepath):
    """Read the cookie data and return a list of cookie dictionaries."""
    cookies = []

    with open(filepath, "r") as cookie_file:
        cookie_data = csv.DictReader(cookie_file)

        for row in cookie_data:
            cookie = {
                "id": int(row["id"]),
                "title": row["title"],
                "description": row["description"],
                "price": float(row["price"].replace("$", "")),
                "sugar_free": row["sugar_free"].lower() == "yes",
                "gluten_free": row["gluten_free"].lower() == "yes",
                "contains_nuts": row["contains_nuts"].lower() == "yes",
            }
            cookies.append(cookie)

    return cookies


def ask_yes_or_no(question):
    """Ask a yes-or-no question until the user gives a valid answer."""
    while True:
        answer = input(question).strip().lower()

        if answer in ["yes", "y"]:
            return True
        if answer in ["no", "n"]:
            return False

        print('Please answer "yes", "y", "no", or "n".')


def welcome():
    """Print the welcome message and ask about dietary restrictions."""
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.\n")
    print(
        "We'd hate to trigger an allergic reaction in your body. "
        "So please answer the following questions:\n"
    )

    allergic_to_nuts = ask_yes_or_no("Are you allergic to nuts? ")
    allergic_to_gluten = ask_yes_or_no("Are you allergic to gluten? ")
    avoiding_sugar = ask_yes_or_no("Do you suffer from diabetes? ")

    return {
        "nuts": allergic_to_nuts,
        "gluten": allergic_to_gluten,
        "sugar": avoiding_sugar,
    }


def display_cookies(cookies, dietary_needs):
    """Display and return only cookies that meet the customer's needs."""
    suitable_cookies = []

    for cookie in cookies:
        has_conflict = (
            (dietary_needs["nuts"] and cookie["contains_nuts"])
            or (dietary_needs["gluten"] and not cookie["gluten_free"])
            or (dietary_needs["sugar"] and not cookie["sugar_free"])
        )

        if not has_conflict:
            suitable_cookies.append(cookie)

    restrictions = []
    if dietary_needs["nuts"]:
        restrictions.append("nuts")
    if dietary_needs["gluten"]:
        restrictions.append("gluten")
    if dietary_needs["sugar"]:
        restrictions.append("sugar")

    if restrictions:
        restriction_text = " or ".join(restrictions)
        print(
            f"\nGreat! Here are the cookies without {restriction_text} "
            "that we think you might like:\n"
        )
    else:
        print("\nGreat! Here are the cookies we think you might like:\n")

    for cookie in suitable_cookies:
        print(f"#{cookie['id']} - {cookie['title']}")
        print(cookie["description"])
        print(f"Price: ${cookie['price']:.2f}\n")

    return suitable_cookies


def get_cookie_from_dict(id, cookies):
    """Find and return a cookie with the given id."""
    for cookie in cookies:
        if cookie["id"] == id:
            return cookie


def solicit_quantity(id, cookies):
    """Ask for and validate the quantity of a selected cookie."""
    cookie = get_cookie_from_dict(id, cookies)

    while True:
        answer = input(
            f"My favorite! How many {cookie['title']}s would you like? "
        )

        try:
            quantity = int(answer)
            if quantity > 0:
                break
        except ValueError:
            pass

        print("Please enter a positive whole number.")

    subtotal = quantity * cookie["price"]
    print(
        f"Your subtotal for {quantity} {cookie['title']} is ${subtotal:.2f}."
    )
    return quantity


def solicit_order(cookies):
    """Take and validate all parts of the customer's order."""
    order = []
    finish_words = ["finished", "done", "quit", "exit"]
    first_cookie = True

    while True:
        if first_cookie:
            prompt = (
                "Please enter the number of any cookie you would like to purchase: "
            )
        else:
            prompt = (
                "Please enter the number of any other cookie you would like to "
                'purchase (type "finished" if finished with your order): '
            )

        answer = input(prompt).strip().lower()

        if answer in finish_words:
            break

        try:
            cookie_id = int(answer)
        except ValueError:
            print("Please enter a valid cookie number.")
            continue

        if get_cookie_from_dict(cookie_id, cookies) is None:
            print("Please choose one of the cookie numbers shown above.")
            continue

        quantity = solicit_quantity(cookie_id, cookies)
        order.append({"id": cookie_id, "quantity": quantity})
        first_cookie = False

    return order


def display_order_total(order, cookies):
    """Print the completed order and total price."""
    print("\nThank you for your order. You have ordered:\n")

    total = 0
    for item in order:
        cookie = get_cookie_from_dict(item["id"], cookies)
        print(f"-{item['quantity']} {cookie['title']}")
        total += item["quantity"] * cookie["price"]

    print(f"\nYour total is ${total:.2f}.")
    print("Please pay with Bitcoin before picking-up.\n")
    print("Thank you!")
    print("-The Python Cookie Shop Robot.")


def run_shop(cookies):
    """Run the extra credit cookie shop."""
    dietary_needs = welcome()
    suitable_cookies = display_cookies(cookies, dietary_needs)
    order = solicit_order(suitable_cookies)
    display_order_total(order, suitable_cookies)
