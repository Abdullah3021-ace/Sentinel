from pricing import apply_tax

def checkout(subtotal, region):
    total = apply_tax(subtotal, region)
    return total
