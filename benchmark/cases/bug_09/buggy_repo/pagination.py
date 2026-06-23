def get_page_items(items, page_number, page_size):
    start = page_number * page_size
    end = start + page_size
    return items[start:end]

def fetch_last_page(items, page_size):
    total_pages = len(items) // page_size
    return get_page_items(items, total_pages, page_size)
