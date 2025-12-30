import secrets
import string


def generate_ai_secure_code():
    length = secrets.choice(range(6, 16))  # Random length between 6 and 16

    char = (
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
        + "!@#$%^&*()-_=+[]{}<>?"
    )

    while True:
        code = "".join(secrets.choice(char) for _ in range(length))

        if (
            any(c.isupper() for c in code)
            and any(c.islower() for c in code)
            and any(c.isdigit() for c in code)
            and any(c in "!@#$%^&*()-_=+[]{}<>" for c in code)
        ):
            return code
