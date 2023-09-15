import discord
from discord.ext import commands
from discord import app_commands

from config import Config

import requests
import json
import datetime
import pprint


class Learning_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE

    def getHomework(self):
        headers = {'Authorization': f"Bearer {self.token}",
                   'Content-Type': 'application/json',
                   'Notion-Version': '2022-06-28'}
        search_params = {"filter": {"value": "page", "property": "object"}}

        request_list = requests.post(
            'https://api.notion.com/v1/search',
            json=search_params, headers=headers).json()['results']

        homework_list = ""

        for homework in request_list:
            pprint.pp(homework)
            homework_data = self.GetHomeworkData(homework)

            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            if homework_data['date'] == str(tomorrow):
                homework_list += "- " + \
                    homework_data['name'] + " " + \
                    f"**{homework_data['type']}**"

        if len(homework_list) > 0:
            return homework_list
        else:
            return None

    def GetHomeworkData(self, result):
        # you can print result here and check the format of the answer.
        homework_id = result['id']
        properties = result['properties']
        date = properties['Date']['date']['start']
        name = properties['Name']['title'][0]['text']['content']
        type = properties['Type']['select']['name']

        return {
            'id': homework_id,
            'date': date,
            'name': name,
            'type': type,
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded learning_system.py!')

    @app_commands.command(name="zadania", description="See what is for tomorrow homework")
    async def zadania(self, interaction: discord.Interaction):
        homework = self.getHomework()
        if homework is None:
            await self.bot.embed(interaction, "", title="There is no homework for tomorrow <:pog:1007719591276990655>")
        else:
            await self.bot.embed(interaction, homework, title="Homework for tomorrow:")


async def setup(bot):
    await bot.add_cog(Learning_system(bot))
