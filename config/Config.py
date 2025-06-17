from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    API_URL: str = os.getenv("API_URL")
    PAGE_SIZE: int = int(os.getenv("MOVIE_PAGE_SIZE"))


config = Config()
