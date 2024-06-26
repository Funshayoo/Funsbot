import discord
from discord.ext import commands
from discord import app_commands

import random


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # self.blacklisted = set(open("./src/blacklisted_words.txt"))
        self.blacklisted = open(
            "src/blacklisted_words.txt").read().splitlines()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    @commands.Cog.listener()
    async def on_message(self, message):

        for word in self.blacklisted:
            if (word.lower().strip() in str(message.content).lower().strip()):
                await message.add_reaction('💀')
                await message.reply("https://tenor.com/view/rotating-skull-gif-24524852")
            else:
                pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
