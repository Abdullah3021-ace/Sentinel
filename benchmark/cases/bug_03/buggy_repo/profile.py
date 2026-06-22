def get_display_name(user):
    return user["name"].strip().title()

def render_profile(user):
    name = get_display_name(user)
    return f"Welcome, {name}"
