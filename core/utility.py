# -*- coding: utf-8 -*-
import re


EMAIL_REGEX_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_email(email: str) -> bool:
    """
    Validates the email format using a regular expression pattern.
    Returns True if the email is valid, False otherwise.
    """
    return re.match(EMAIL_REGEX_PATTERN, email) is not None


def check_password_strength(password: str) -> (bool, str):
    if len(password) < 6:
        return False, "password is less than 6 characters"

    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        return False, "Must contain one lower case and one upper case character"

    if not re.search(r"\d", password):
        return False, "Must contain at least one digit."

    return True, "Strong Password"
