import discord
from discord.ext import commands
from discord import app_commands
import random

dictionary = open("./wordle_src/wordle_words.txt")


async def get_random_word():
    with open("./wordle_src/wordle_words.txt") as f:
        wordle_word = f.read().splitlines()
        return random.choice(wordle_word)


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
        word = await get_random_word()
        embed = discord.Embed(title="Comming soon :eyes:",
                              description=f"For now here's your word {word}", color=self.color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Wordle(bot))
