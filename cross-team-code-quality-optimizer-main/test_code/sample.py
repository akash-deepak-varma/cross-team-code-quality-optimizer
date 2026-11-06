def process_order(order, user, discount, payment):
    if order:
        if user:
            if payment:
                if discount:
                    total = order["price"] - discount
                else:
                    total = order["price"]

                if total > 1000:
                    print("Large order")
                else:
                    print("Normal order")

                if user["active"]:
                    print("Active user")

                return total

    return 0