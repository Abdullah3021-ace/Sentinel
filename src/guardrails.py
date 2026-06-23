import re

DANGEROUS_PATTERNS = [
    r'rm\s+-rf', r'\bsudo\b', r'\bos\.system\(',
    r'\bsubprocess\.(run|call|Popen)\(', r'\beval\(', r'\bexec\(',
    r'DROP\s+TABLE', r'DELETE\s+FROM.+WHERE\s+1\s*=\s*1',
]


class UnsafePatchError(Exception):
    pass


def check_patch_safety(new_code: str):
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, new_code, re.IGNORECASE):
            raise UnsafePatchError(
                f'Blocked: matched dangerous pattern {pattern!r}')
