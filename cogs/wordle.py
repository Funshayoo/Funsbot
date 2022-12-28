import discord
from discord.ext import commands
from discord import app_commands
import random

dictionary = set(word.strip() for word in open("/wordle_src/wordle_words.txt"))


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @app_commands.command(name="wordle", description="Play a game of wordle")
    async def wordle(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Comming soon :eyes:",
                              description="", color=self.color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Wordle(bot))
