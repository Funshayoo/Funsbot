import discord
from discord.ext import commands
from discord import app_commands

import random
from jokeapi import Jokes


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.flip_array = ['orzeł!', 'reszka!']

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

    # ? flip command

    @app_commands.command(name="moneta", description="rzut monetą")
    async def moneta(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, random.choice(self.flip_array))

    # @app_commands.command(name="zarcik", description="zarcik kosmonaucik (niestety tylko po ang, ale z czasem zmienie jezyk na polski)")
    # async def zarcik(self, interaction: discord.Interaction):
    #     j = await Jokes()
    #     joke = await j.get_joke(response_format="txt", lang="en", category=['dark'])
    #     await self.bot.embed(interaction, joke)


async def setup(bot):
    await bot.add_cog(Fun(bot))
