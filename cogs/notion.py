import discord
from discord.ext import commands
from discord import app_commands

from config import Config

import requests
import datetime


def get_next_week_day():
    today = datetime.datetime.today()
    next_weekday = None
    if today.weekday() < 4 or today.weekday() == 6:
        # show next day homework
        next_weekday = today + datetime.timedelta(days=1)
    else:
        # show next monday homework
        monday = 0
        days = (monday - today.weekday() + 7) % 7
        next_weekday = today + datetime.timedelta(days=days)

    return str(next_weekday.date())


def format_homework(id, name, type):
    link_name = str(name).replace('.', '-').replace(' ', '-')
    link_id = str(id).replace('-', '')

    link = f"https://funshayo.notion.site/{link_name}-{link_id}?pvs=4"

    formatted_homework = f"- [{name}]({link})" + ' ' \
        f"**{type}**" + '\n'
    return formatted_homework


def getHomework(groups):
    token = Config.NOTION_TOKEN
    headers = {'Authorization': f"Bearer {token}",
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
                homework_data = GetHomeworkData(homework)
            except Exception as e:
                print(e)
                continue

            next_weekday = get_next_week_day()
            if homework_data['date'] == next_weekday and (homework_data['group'] in groups or homework_data['group'] == "wszyscy"):
                formatted_homework = format_homework(
                    homework_data['id'], homework_data['name'], homework_data['type'])
                homework_list += formatted_homework

    if len(homework_list) > 0:
        return homework_list
    else:
        return None


def GetHomeworkData(result):
    # you can print result here and check the format of the answer.
    homework_id = result['id']
    properties = result['properties']
    date = properties['Date']['date']['start']
    name = properties['Name']['title'][0]['text']['content']
    type = properties['Type']['select']['name']
    group = properties['Grupa']['select']['name']

    return {
        'id': homework_id,
        'date': date,
        'name': name,
        'type': type,
        'group': group,
    }


class GroupView(discord.ui.View):
    groups = None

    @discord.ui.select(
        placeholder="W ktorych grupach jestes?",
        options=[
            discord.SelectOption(label="grupa 1 angielski",
                                 value="1ang", emoji="🇬🇧"),
            discord.SelectOption(label="grupa 2 angielski",
                                 value="2ang", emoji="🇬🇧"),

            discord.SelectOption(label="grupa 1 niemiecki",
                                 value="1nie", emoji="🇩🇪"),
            discord.SelectOption(label="grupa 2 niemiecki",
                                 value="2nie", emoji="🇩🇪"),

            discord.SelectOption(
                label="grupa 1 utk", value="1utk", emoji="<:plachta:1153392430054387742>"),
            discord.SelectOption(
                label="grupa 2 utk", value="2utk", emoji="<:okrajni:1153765701878829147>"),
            discord.SelectOption(
                label="grupa 3 utk", value="3utk", emoji="<:pudelko:1153393507004854372>"),

            discord.SelectOption(
                label="religia", value="rel", emoji="✝"),

        ],
        max_values=4
    )
    async def select_callback(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.groups = select_item.values
        homework = getHomework(self.groups)

        embed = discord.Embed(color=0x2F3136)
        embed.description = "[*Lista zadań*](https://funshayo.notion.site/ZS-lista-cb49825d92a7466b80e4621f94e7f04d?pvs=4)\n"
        embed.description += "[*Sprawozdanka*](https://sprawozdanka.ct8.pl/)\n"

        if homework is None:
            embed.title = "Na jutro nie ma zadnych zadan <:najman:1150035175300923502>"
        else:
            embed.description += homework
            embed.title = "Zadania:"
        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
        self.stop()


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    @ app_commands.command(name="zadania", description="Zobacz zapowiedziane zadania")
    async def zadania(self, interaction: discord.Interaction):
        view = GroupView()
        await interaction.response.send_message(view=view, ephemeral=True)
        await view.wait()


async def setup(bot):
    await bot.add_cog(Notion(bot))
