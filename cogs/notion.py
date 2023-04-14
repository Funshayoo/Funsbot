import discord
from discord.ext import commands
from discord import app_commands

from config import Config

import requests
import json
import datetime


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE

    def getHomework(self):
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'

        r = requests.post(url, headers={
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2021-08-16"
        })

        result_dict = r.json()
        homework_list_result = result_dict['results']

        homework_list = []

        for homework in homework_list_result:
            homework_dict = self.mapNotionResultToHomework(homework)

            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            if homework_dict['date'] == str(tomorrow):
                homework_list.append(homework_dict['name'] + " " + f"**{homework_dict['type']}**")

        homework_list = self.format_homework(homework_list)

        return homework_list

    def mapNotionResultToHomework(self, result):
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

    # def bubble_sort(self, array):
    #     n = len(array)
    #     for i in range(n):
    #         for j in range(0, n - i - 1):
    #             if array[j] > array[j + 1]:
    #                 array[j], array[j + 1] = array[j + 1], array[j]
    #     return array

    def format_homework(self, homework):
        homework_formatted = ""
        for word in homework:
            homework_formatted += f"- {word}\n"
        return homework_formatted

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    @app_commands.command(name="zadania", description="See what is for tomorrow homework")
    @app_commands.checks.has_role("8c")
    async def zadania(self, interaction: discord.Interaction):
        homework = self.getHomework()
        if len(homework) == 0:
            await self.bot.embed(interaction, "", title="There is no homework for tomorrow :smile:")
        else:
            await self.bot.embed(interaction, homework, title="Homework for tomorrow:")


async def setup(bot):
    await bot.add_cog(Notion(bot))
