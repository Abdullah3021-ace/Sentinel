def parse_amount(raw_value):
    try:
        return int(raw_value)
    except TypeError:
        return 0

def handle_input(raw_value):
    return parse_amount(raw_value)
