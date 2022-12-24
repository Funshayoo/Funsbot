import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

intents = discord.Intents().all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # ? cut off the .py from the file name
            await bot.load_extension(f'cogs.{filename[:-3]}')

# ? changes bot activity to $help


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='/help'))
    print('Bot is ready!')
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)

# ? on join message + add role


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1007632094899490886)
    embed = discord.Embed(
        title='Siemanoo!!!',
        description=f'{member.mention} <:pepewow:1007638216033194064>')
    await channel.send(embed=embed)
    role = discord.utils.get(member.guild.roles, name='Paczka')
    await member.add_roles(role)


# ? Checks for the messages


@bot.event
async def on_message(message):
    answ = ['gówno jeden zero', 'jajco', 'chujów sto']
    qstn = ['co', '?', 'co?', 'Co', 'Co?']

    if (message.author == bot):
        return
    elif message.content in qstn:
        await message.channel.send(random.choice(answ))

    #! allow using commands
    await bot.process_commands(message)

# ? help command


@bot.tree.command(name="help", description="use this command to get some help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="", description="You can use commands by typing /**command**", color=0xffffff)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ! starts the bot


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)
asyncio.run(main())
