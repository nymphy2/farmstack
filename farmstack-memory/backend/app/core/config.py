import os
import secrets

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()

client_id = os.environ.get('CLIENT_ID')
db_url = os.environ.get('DB_URL')


class Settings(BaseSettings):
    DB_URL: str = db_url
    CLIENT_ID: str = client_id
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # expire time = 60m * 24h = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()
