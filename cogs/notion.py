import discord
from discord.ext import commands
from notion_client import Client
from discord.ext.commands import has_permissions
from discord import app_commands

client = Client(auth='secret_3yTWYhfWs8LbI08eE8Pu5u1DYNbZy5SK9BYUxzqSXcoN')
#database id = e63f878470b44afcb35ae40ef4a2b5f8

class Notion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    @app_commands.command(name="zadania", description ="Prints the tomorow homework from notion database")
    @app_commands.checks.has_role("8c")
    async def clear(self, interaction):
        await interaction.response.send_message('test')

async def setup(client):
    await client.add_cog(Notion(client))