def check_stock(quantity, threshold):
    if quantity > threshold:
        return "low_stock"
    return "ok"

def process_order(quantity, threshold):
    status = check_stock(quantity, threshold)
    return status
