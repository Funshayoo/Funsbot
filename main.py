
import discord
from discord import app_commands
from discord.ext import commands

import asyncio
import random

import os
from dotenv import load_dotenv


class Funsbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_color = 0x2F3136

    async def embed(self, interaction: discord.Interaction, description: str, title: str = None,  ephemeral: bool = False):
        embed = discord.Embed(
            description=description, color=self.embed_color)
        if title is not None:
            embed.title = title

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


# * all needed variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
bot = Funsbot(command_prefix="/", intents=intents, help_command=None)
tree = bot.tree

color = bot.embed_color


async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # ? cut off the .py from the file name
            await bot.load_extension(f'cogs.{filename[:-3]}')

# ? when bot is ready


@bot.event
async def on_ready():
    # ? change bot activity
    await bot.change_presence(activity=discord.Game(name='/help'))
    # ? print message
    print(f"""
     ______               _           _   
    |  ____|             | |         | |  
    | |__ _   _ _ __  ___| |__   ___ | |_ 
    |  __| | | | '_ \/ __| '_ \ / _ \| __|
    | |  | |_| | | | \__ \ |_) | (_) | |_ 
    |_|   \__,_|_| |_|___/_.__/ \___/ \__|

        made by Funshayo
        Logged in as: {bot.user}
        Discord version: {discord.__version__} 
    """)
    # ! sync all commands
    try:
        await tree.sync()
    except Exception as e:
        print(e)

# ? on member join


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1007632094899490886)
    embed = discord.Embed(
        title='Siemanoo!!!', description=f'{member.mention} <:pepewow:1007638216033194064>', color=color)
    # ? send welcome message + add user role
    await channel.send(embed=embed)
    role = discord.utils.get(member.guild.roles, name='Paczka')
    await member.add_roles(role)


# ? help command


@tree.command(name="help", description="use this command to get some help")
async def help(interaction: discord.Interaction):
    await bot.embed(interaction, "You can use commands by typing /**command**", ephemeral=True)


# ! starts the bot


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)
asyncio.run(main())
