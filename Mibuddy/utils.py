import string
import random
import re


def generate_random_string(length=40):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def is_valid_email(email):
    return re.fullmatch('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email) is not None
