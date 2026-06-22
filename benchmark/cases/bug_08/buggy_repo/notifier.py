def send_notification(user_id, message):
    try:
        deliver(user_id, message)
    except Exception:
        pass

def deliver(user_id, message):
    if not user_id:
        raise ValueError("user_id is required")
    return True
