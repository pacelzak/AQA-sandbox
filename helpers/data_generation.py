import random
import string

from faker import Faker

fake = Faker()

USERNAME_ALPHABET = string.ascii_lowercase + string.digits + "_"
EMAIL_ALPHABET = string.ascii_lowercase + string.digits
EMAIL_DOMAIN = "example.com"


def _random_string(length: int, alphabet: str) -> str:
    if length < 1:
        raise ValueError(f"length must be >= 1, got {length}")
    return "".join(random.choices(alphabet, k=length))


class DataGenerator:
    def __init__(
        self,
        username_len: int | None = None,
        email_len: int | None = None,
        password_len: int | None = None,
        display_name_len: int | None = None,
        bio_len: int | None = None,
    ):
        self.username = self.make_username(username_len)
        self.email = self.make_email(email_len)
        self.password = self.make_password(password_len)
        self.display_name = self.make_display_name(display_name_len)
        self.bio = self.make_bio(bio_len)

    @staticmethod
    def make_username(length: int | None = None) -> str:
        if length is None:
            return fake.bothify(text="user_########")
        return _random_string(length, USERNAME_ALPHABET)

    @staticmethod
    def make_email(length: int | None = None) -> str:
        """length: общая длина email вместе с @domain."""
        if length is None:
            return fake.email()
        local_len = length - len(EMAIL_DOMAIN) - 1  # -1 за "@"
        if local_len < 1:
            raise ValueError(f"email length must be >= {len(EMAIL_DOMAIN) + 2}")
        return f"{_random_string(local_len, EMAIL_ALPHABET)}@{EMAIL_DOMAIN}"

    @staticmethod
    def make_password(length: int | None = None) -> str:
        return fake.password() if length is None else fake.password(length=length)

    @staticmethod
    def make_display_name(length: int | None = None) -> str:
        if length is None:
            return fake.name()
        return _random_string(length, string.ascii_letters)

    @staticmethod
    def make_bio(length: int | None = None) -> str:
        if length is None:
            return fake.text(max_nb_chars=200)
        return _random_string(length, string.ascii_letters)