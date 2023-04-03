import discord
from discord.ext import commands
from discord import app_commands

import random


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.flip_array = ['heads!', 'tails!']

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    @commands.Cog.listener()
    async def on_message(self, message):
        # ? funni gówno joke
        answer_array = ['gówno jeden zero', 'jajco', 'chujów sto']
        co_array = ['co', 'co?']

        if (message.author == self.bot):
            return
        elif message.content.lower() in co_array:
            embed = discord.Embed(title="", description=random.choice(
                answer_array), color=self.bot_embed_color)
            await message.reply(embed=embed)

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


async def setup(bot):
    await bot.add_cog(Fun(bot))
