import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv


class Funsbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_color = 0x2F3136


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
    print(f'Logged in as: {bot.user}')
    print(f'Discord version: {discord.__version__} ')
    # ! sync all commands
    try:
        guild_id = 1007631720155205632
        await tree.sync(guild=discord.Object(guild_id))
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


# ? on message event


@bot.event
async def on_message(message):
    # ? funni gówno joke
    answ = ['gówno jeden zero', 'jajco', 'chujów sto']
    qstn = ['co', '?', 'co?', 'Co', 'Co?']

    if (message.author == bot):
        return
    elif message.content in qstn:
        await message.channel.send(random.choice(answ))

    #! allow using prefix commands
    await bot.process_commands(message)

# ? help command


@tree.command(name="help", description="use this command to get some help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        description="You can use commands by typing /**command**", color=color)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ! starts the bot


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)
asyncio.run(main())
