import re

def validate_input(text: str, min_length: int = 3, max_length: int = 500):

    # empty check
    if not text or text.strip() == "":
        return False, "Input empty irukka koodadhu"

    text = text.strip()

    # length check
    if len(text) < min_length:
        return False, f"Minimum {min_length} characters venum"

    if len(text) > max_length:
        return False, f"Maximum {max_length} characters mattum allow"

    # invalid characters check
    if not re.match(r"^[a-zA-Z0-9\s.,!?@#&()\-_%]+$", text):
        return False, "Invalid characters irukku"

    # spam / repetitive check
    if len(set(text)) < 3:
        return False, "Romba repetitive text irukku"

    return True, "Valid input"