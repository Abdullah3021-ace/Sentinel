def apply_tax(subtotal, region):
    rate = get_tax_rate(region)
    return subtotal + (subtotal * rate)

def get_tax_rate(region):
    rates = {"US": 0.07, "CA": 0.13}
    return rates[region]
