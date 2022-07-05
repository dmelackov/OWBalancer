import os
import secrets

DB_NAME = os.environ.get("DATABASE_TABLE", "owbalancer")
db_type = os.environ.get("DATABASE_TYPE", "sqlite")
secretKey = os.environ.get("SECRET_KEY", None)
if secretKey is None:
    try:
        with open("secret.txt") as f:
            secretKey = f.readline()
    except FileNotFoundError:
        with open("secret.txt", mode="w") as f:
            secretKey = secrets.token_urlsafe(16)
            f.write(secretKey)
host = os.environ.get("DATABASE_IP", "127.0.0.1")
port = int(os.environ.get("DATABASE_PORT", "3306"))
user = os.environ.get("DATABASE_USER_USERNAME", "root")
password = os.environ.get("DATABASE_USER_PASSWORD", "root")
site_port = int(os.environ.get("SITE_PORT", "8080"))
debug = bool(os.environ.get("SITE_PORT", "False"))