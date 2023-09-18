import discord
from discord.ext import commands
from discord import app_commands

from config import Config

import requests
import datetime


class Learning_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = Config.NOTION_TOKEN

    def format_homework(self, id, name, type):
        link_name = str(name).replace('.', '-').replace(' ', '-')
        link_id = str(id).replace('-', '')

        link = f"https://funshayo.notion.site/{link_name}-{link_id}?pvs=4"

        formatted_homework = f"- [{name}]({link})" + ' ' \
            f"**{type}**" + '\n'
        return formatted_homework

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
            if homework['parent']['type'] == "workspace":
                pass
            else:
                try:
                    homework_data = self.GetHomeworkData(homework)
                except Exception as e:
                    print(e)
                    continue

                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                if homework_data['date'] == str(tomorrow):
                    formatted_homework = self.format_homework(
                        homework_data['id'], homework_data['name'], homework_data['type'])
                    homework_list += formatted_homework

        if len(homework_list) > 0:
            return homework_list
        else:
            return None

    def GetHomeworkData(self, result):
        # you can print result here and check the format of the answer.
        homework_id = result['id']
        print(homework_id)
        properties = result['properties']
        print(properties)
        date = properties['Date']['date']['start']
        print(date)
        name = properties['Name']['title'][0]['text']['content']
        print(name)
        type = properties['Type']['select']['name']
        print(type)

        return {
            'id': homework_id,
            'date': date,
            'name': name,
            'type': type,
        }

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded learning_system.py!')

    @ app_commands.command(name="zadania", description="Zobacz zapowiedziane zadania na jutro")
    async def zadania(self, interaction: discord.Interaction):
        await interaction.response.defer()
        homework = self.getHomework()
        if homework is None:
            await self.bot.embed(interaction, "", title="Nie ma nic na jutro <:najman:1150035175300923502>", followup=True)
        else:
            await self.bot.embed(interaction, homework, title="Zadania na jutro:", followup=True)


async def setup(bot):
    await bot.add_cog(Learning_system(bot))
