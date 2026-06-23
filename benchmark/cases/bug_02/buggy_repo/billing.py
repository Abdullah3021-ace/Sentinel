def calculate_total(price, quantity):
    return price * quantity

def apply_discount(price, quantity, discount_code):
    if isinstance(price, str): price = float(price)
if isinstance(quantity, str): quantity = float(quantity)
total = calculate_total(price, quantity)
    return total
