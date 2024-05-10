import os

from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    telebot_token: SecretStr


settings = Settings(
    telebot_token=os.getenv("TELEBOT_TOKEN")
)
