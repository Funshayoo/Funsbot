import discord
from discord.ext import commands
from discord import app_commands
import random

# * flip array
flip_var = ['heads!', 'tails!']
color = 0x2F3136


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded fun.py!')

    # ? flip command
    @app_commands.command(name="flip", description="Flip a coin")
    async def flip(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="", description=random.choice(flip_var), color=color)
        await interaction.response.send_message(embed=embed)

    # ? bitches command
    @app_commands.command(name="bitches", description="Funni")
    async def bitches(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="", description="No bitches <:KEKW:1007719515620126852>", color=color)
        await interaction.response.send_message(embed=embed)

    # ? manho command

    @app_commands.command(name="manho", description="<3 manho")
    async def manho(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description="Kocham manho <:PepeHappy:1007638220131024997>", color=color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
