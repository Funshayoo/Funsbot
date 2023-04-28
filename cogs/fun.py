import discord
from discord.ext import commands
from discord import app_commands

import random

from jokeapi import Jokes


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.flip_array = ['heads!', 'tails!']

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ? funni gówno joke
        answer_array = ['gówno jeden zero', 'jajco', 'chujów sto']
        co_array = ['co', 'co?']

        if message.author.bot:
            return

        elif message.content.lower() in co_array:
            await message.channel.send(random.choice(answer_array))

    # ? flip command
    @app_commands.command(name="flip", description="Flip a coin")
    async def flip(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, random.choice(self.flip_array))

    # ? bitches command
    @app_commands.command(name="bitches", description="Funni")
    async def bitches(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "No bitches <:KEKW:1007719515620126852>")

    # ? manho command
    @app_commands.command(name="manho", description="<3 manho")
    async def manho(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "Kocham manho <:PepeHappy:1007638220131024997>")

    @app_commands.command(name="joke", description="Bot will tell you the joke")
    async def joke(self, interaction: discord.Interaction):
        j = await Jokes()
        joke = await j.get_joke(response_format="txt", lang="en", category=['dark'])
        await self.bot.embed(interaction, joke, title="Joke:")


async def setup(bot):
    await bot.add_cog(Fun(bot))
