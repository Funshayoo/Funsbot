from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Config:
    DISCORD_TOKEN = getenv("DISCORD_TOKEN")
    DISCORD_ANNOUNCEMENT_CHANNEL = getenv("DISCORD_ANNOUNCEMENT_CHANNEL")

    DATABASE_DIRECTORY = getenv("DATABASE_DIRECTORY")

    NOTION_TOKEN = getenv("NOTION_TOKEN")
    NOTION_DATABASE_ID = getenv("NOTION_DATABASE_ID")
    NOTION_DATABASE = getenv("NOTION_DATABASE")

    # OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    # SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
    # SPOTIFY_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
