from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    BASE_URL = os.getenv("BASE_URL")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_NAME = os.getenv("ADMIN_NAME")
    DISPLAY_NAME = os.getenv("DISPLAY_NAME")
    MOD_EMAIL = os.getenv("MOD_EMAIL")
    MOD_PASSWORD = os.getenv("MOD_PASSWORD")
    ACTIVE_EMAIL = os.getenv("ALICE_EMAIL")
    ACTIVE_PASSWORD = os.getenv("ALICE_PASSWORD")
    BOB_EMAIL = os.getenv("BOB_EMAIL")
    BOB_PASSWORD = os.getenv("BOB_PASSWORD")
    CAROL_EMAIL = os.getenv("CAROL_EMAIL")
    CAROL_PASSWORD = os.getenv("CAROL_PASSWORD")
    PRIVATE_EMAIL = os.getenv("DAVE_EMAIL")
    PRIVATE_PASSWORD = os.getenv("DAVE_PASSWORD")
    NEW_EMAIL = os.getenv("EVE_EMAIL")
    NEW_PASSWORD = os.getenv("EVE_PASSWORD")
    BANNED_EMAIL = os.getenv("FRANK_EMAIL")
    BANNED_PASSWORD = os.getenv("FRANK_PASSWORD")
    CONNECTION_BD = os.getenv("CONNECTION_BD")
    RESET_URL = os.getenv("RESET_URL")