Category: missing null check. user['name'] can be None, and .strip() is called on it without checking first.
