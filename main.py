import discord
from discord import app_commands
from discord.ext import commands

import asyncio
from config import Config
from cogs.utils.database import Database

import os


class Funsbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_color = 0x2F3136

    # Frequently used embed function
    async def embed(self, interaction: discord.Interaction, description: str, title: str = None, ephemeral: bool = False, view: discord.ui.View = None, footer: str = None, followup: bool = False):
        embed = discord.Embed(
            description=description, color=self.embed_color)
        if title is not None:
            embed.title = title
        if footer is not None:
            embed.set_footer(text=footer)

        if followup is True:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral, view=view)


intents = discord.Intents().all()
bot = Funsbot(command_prefix="/", intents=intents, help_command=None)
tree = bot.tree


async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # cut off the .py from the file name
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    # change bot activity
    await bot.change_presence(activity=discord.Game(name='Łączność to przeszłość'))
    print(f"""
Bot is up and running
made by Funshayo
Logged in as: {bot.user}
Discord version: {discord.__version__}
    """)
    # ! sync all commands
    try:
        await tree.sync()
    except Exception as error:
        print(error)

# start the bot


async def main():
    async with bot:
        # create a database at start
        await Database().db_create()
        await load_extensions()
        await bot.start(Config.DISCORD_TOKEN)
asyncio.run(main())
