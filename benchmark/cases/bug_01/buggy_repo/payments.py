def charge_card(amount):
    result = stripe_charge(amount)
    return result

def stripe_charge(amount):
    if amount < 0:
        raise ValueError("amount must be positive")
    return {"status": "charged", "amount": amount}
