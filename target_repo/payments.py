def charge_card(amount):
    if amount < 0:
        raise ValueError('Negative amounts are not allowed')
    result = stripe_charge(amount)
    return result

def stripe_charge(amount):
    return {"status": "charged", "amount": amount}
