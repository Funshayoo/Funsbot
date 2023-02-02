import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions

from notion_client import Client
from config import Config


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    @app_commands.command(name="zadania", description="See what is for tommorow homework")
    @ app_commands.checks.has_role("8c")
    async def zadania(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "", title="Comming soon :eyes:")


async def setup(bot):
    await bot.add_cog(Notion(bot))
