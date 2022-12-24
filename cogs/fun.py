import discord
from discord.ext import commands
from discord import app_commands
import random

# * flip array
flip_var = ['heads!', 'tails!']


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    # ? flip command
    @app_commands.command(name="flip", description="Flip a coin")
    async def flip(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(flip_var))

    # ? bitches command
    @app_commands.command(name="bitches", description="Funni")
    async def bitches(self, interaction: discord.Interaction):
        await interaction.response.send_message('No bitches <:KEKW:1007719515620126852>')

    # ? manho command

    @app_commands.command(name="manho", description="<3 manho")
    async def manho(self, interaction: discord.Interaction):
        await interaction.response.send_message('Kocham manho <:PepeHappy:1007638220131024997>')


async def setup(bot):
    await bot.add_cog(Fun(bot))
