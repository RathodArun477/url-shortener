# A util file that generates a code for the url using secrets and string library

import secrets
import string
from urllib.parse import urlparse

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

def normalize_url(url: str):
    """
    Validates and normalizes a given URL.
    - Adds https:// if scheme is missing.
    - Rejects invalid schemes (only http and https allowed).
    - Ensures valid host/domain name exists.
    Returns normalized URL string, or None if invalid.
    """
    if not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None

    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None

    return url
