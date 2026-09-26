import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
SKU_PATTERN = re.compile(r"^[A-Z0-9\-]{3,64}$")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))

def is_valid_sku(sku: str) -> bool:
    return bool(SKU_PATTERN.match(sku.upper()))
