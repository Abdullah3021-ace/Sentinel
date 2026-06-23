Category: off-by-one boundary error. Integer division for total_pages doesn't round up, and page_number isn't converted to zero-indexed for the last page.
