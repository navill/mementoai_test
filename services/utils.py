import base64
import hashlib

from random_strings import random_string


def create_shorten_key(url):
    salt = random_string(8)
    hashed = hashlib.sha3_256(f"{url}{salt}".encode()).digest()
    return base64.urlsafe_b64encode(hashed).decode()[:10]
