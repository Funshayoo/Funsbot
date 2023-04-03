import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions

from config import Config

import requests
import json


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE_ID
        self.update_DB_URL = f'https://api.notion.com/v1/databases/{self.database_id}'
        self.db_data = None

        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"}

    def read_database(self, database_id, headers):
        readUrl = f"https://api.notion.com/v1/databases/{database_id}/query"

        res = requests.request("POST", readUrl, headers=headers)
        data = res.json()
        print(res.status_code)

        with open('./notion.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)

        return data

    def get_tasks_from_db(self, db_data):
        length_of_table = len(db_data["results"])
        for i in range(length_of_table):
            if len(db_data["results"][i]["properties"]["Task"]["title"]) != 0:
                task_name = db_data["results"][i]["properties"]["Task"]["title"][0]["plain_text"]
                print(f"{i} - {task_name}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.db_data = self.read_database(self.database_id, self.headers)
        print(self.get_tasks_from_db(self.db_data))

        print('Loaded notion.py!')

    @app_commands.command(name="zadania", description="See what is for tomorrow homework")
    @ app_commands.checks.has_role("8c")
    async def zadania(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "", title="Coming soon :eyes:")


async def setup(bot):
    await bot.add_cog(Notion(bot))
