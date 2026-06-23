Category: multi-file bug. cart.py calls pricing.py's get_tax_rate, which has a hardcoded dict missing the 'UK' key. Fix lives in pricing.py, traceback spans both files.
