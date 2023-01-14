import discord
from discord.ext import commands
from discord import app_commands
import random


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color
        self.flip_array = ['heads!', 'tails!']

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

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
