import os

DB_NAME = os.environ.get("DATABASE_TABLE", "owbalancer")
db_type = os.environ.get("DATABASE_TYPE", "sqlite")
host = os.environ.get("DATABASE_IP", "127.0.0.1")
port = int(os.environ.get("DATABASE_PORT", "3306"))
user = os.environ.get("DATABASE_USER_USERNAME", "root")
password = os.environ.get("DATABASE_USER_PASSWORD", "root")
site_port = int(os.environ.get("SITE_PORT", "8080"))