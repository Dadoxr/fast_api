import os, dotenv
from pathlib import Path


var_path = Path(__file__).resolve().parent
dotenv.load_dotenv(os.path.join(var_path, ".env"))
DEBUG = os.getenv("DEBUG") == "True"

APP_PORT = os.getenv("APP_PORT")


DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DB_DATA = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_DATA}"
ALEMBIC_SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_DATA}"

SECRET_KEY = "fdsfds4f4w"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=90