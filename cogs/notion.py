import discord
from discord.ext import commands
from notion_client import Client
from discord.ext.commands import has_permissions
from discord import app_commands

client = Client(auth='secret_3yTWYhfWs8LbI08eE8Pu5u1DYNbZy5SK9BYUxzqSXcoN')
# database id = e63f878470b44afcb35ae40ef4a2b5f8

color = 0x2F3136


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded notion.py!')

    # TODO finish command + add comments
    @app_commands.command(name="zadania", description="Prints the tomorow homework from notion database")
    @app_commands.checks.has_role("8c")
    async def zadania(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Comming soon",
                              description="", color=color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Notion(bot))
