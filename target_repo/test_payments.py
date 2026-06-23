from payments import charge_card

def test_charge_card_rejects_negative_amount():
    try:
        charge_card(-10)
        assert False, "expected ValueError for negative amount"
    except ValueError:
        pass

def test_charge_card_accepts_positive_amount():
    result = charge_card(10)
    assert result["status"] == "charged"
