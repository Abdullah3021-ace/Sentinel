from shipping import calculate_shipping_cost

def create_order(weight_kg, destination):
    shipping_cost = calculate_shipping_cost(weight_kg, destination)
    return {"shipping_cost": shipping_cost}
