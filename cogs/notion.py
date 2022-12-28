import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from notion_client import Client
from discord.ext.commands import has_permissions
from discord import app_commands

load_dotenv()
notion_client = os.getenv("NOTION_TOKEN")
# database id = e63f878470b44afcb35ae40ef4a2b5f8


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    # TODO finish command + add comments
    @app_commands.command(name="zadania", description="Prints the tomorow homework from notion database")
    @app_commands.checks.has_role("8c")
    async def zadania(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Comming soon :eyes:",
                              description="", color=self.color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Notion(bot))
