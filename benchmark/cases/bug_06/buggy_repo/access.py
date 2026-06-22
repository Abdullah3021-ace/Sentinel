def can_access(user_is_admin, resource_is_private):
    if user_is_admin or resource_is_private:
        return True
    return False

def guard_resource(user_is_admin, resource_is_private):
    allowed = can_access(user_is_admin, resource_is_private)
    return allowed
