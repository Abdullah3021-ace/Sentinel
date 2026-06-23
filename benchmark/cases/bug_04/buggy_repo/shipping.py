def calculate_shipping_cost(weight_kg, destination):
    base_rate = get_base_rate(destination)
    return weight_kg * base_rate

def get_base_rate(destination):
    rates = {"domestic": 2.5, "international": 8.0, "eu": 5.0}
    return rates[destination]
