def calculate_total(price, quantity):
    return price * quantity

def apply_discount(price, quantity, discount_code):
    total = calculate_total(price, quantity)
    return total
