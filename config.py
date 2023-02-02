from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Config:
    DISCORD_TOKEN = getenv("DISCORD_TOKEN")
    NOTION_TOKEN = getenv("NOTION_TOKEN")
    NOTION_DATABASE = getenv("NOTION_DATABASE")
    DATABASE_DIRECTORY = getenv("DATABASE_DIRECTORY")
