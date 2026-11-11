# A util file that generates a code for the url using secrets and string library

import secrets
import string

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))

    return code

# print(generate_code())
# print(generate_code())
# print(generate_code())