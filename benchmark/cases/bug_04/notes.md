Category: multi-file bug. orders.py calls shipping.py's get_base_rate, which has a hardcoded dict missing the 'eu' key. Fix lives in shipping.py, error traceback spans both files.
