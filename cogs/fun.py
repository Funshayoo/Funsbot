import discord
from discord.ext import commands
from discord import app_commands

import random

from jokeapi import Jokes


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.flip_array = ['orzeł!', 'reszka!']

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    # ? flip command
    @app_commands.command(name="moneta", description="rzut monetą")
    async def flip(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, random.choice(self.flip_array))

    @app_commands.command(name="zarcik", description="żarcik kosmonaucik")
    async def joke(self, interaction: discord.Interaction):
        j = await Jokes()
        joke = await j.get_joke(response_format="txt", lang="en", category=['dark'])
        await self.bot.embed(interaction, joke, title="Joke:")


async def setup(bot):
    await bot.add_cog(Fun(bot))
