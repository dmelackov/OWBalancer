import os
import secrets

DB_NAME = os.environ.get("DATABASE_TABLE", "owbalancer")
DB_TYPE = os.environ.get("DATABASE_TYPE", "sqlite")
SECRET_KEY = os.environ.get("SECRET_KEY", None)
if SECRET_KEY is None:
    try:
        with open("secret.txt") as f:
            SECRET_KEY = f.readline()
    except FileNotFoundError:
        with open("secret.txt", mode="w") as f:
            SECRET_KEY = secrets.token_urlsafe(16)
            f.write(SECRET_KEY)
DB_HOST = os.environ.get("DATABASE_IP", "127.0.0.1")
DB_PORT = int(os.environ.get("DATABASE_PORT", "3306"))
DB_USER_LOGIN = os.environ.get("DATABASE_USER_USERNAME", "root")
DB_USER_PASSWORD = os.environ.get("DATABASE_USER_PASSWORD", "root")
SITE_IP = os.environ.get("SITE_IP", "0.0.0.0")
SITE_PORT = int(os.environ.get("SITE_PORT", "8080"))
DEBUG = bool(os.environ.get("DEBUG", "False"))
TRUESKILL_PASSWORD = os.environ.get("TRUESKILL_PASSWORD", "trueskill")