import discord
from discord.ext import commands
from discord import app_commands
import random


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color
        self.is_playing = False
        self.answer = ""
        self.user_quess = ""

        # * all word dictionaries
        self.popular = open("./wordle_src/wordle_words.txt")
        self.all_words = open("./wordle_src/dictionary.txt")

    async def get_random_word(self) -> str:
        wordle_word = self.popular.read().splitlines()
        return random.choice(wordle_word)

    async def generate_blanks(self) -> str:
        return ((":white_medium_square:" * 5) + ("\n")) * 6

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @app_commands.command(name="wordle_play", description="Play a game of wordle")
    async def play_wordle(self, interaction: discord.Interaction):
        self.is_playing = True
        self.answer = await self.get_random_word()
        blanks = await self.generate_blanks()
        embed = discord.Embed(title="Guees the word using: **/wordle_quess**",
                              description=f"{blanks}", color=self.color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wordle_quess", description="Quess a word")
    @app_commands.describe(quess="Your quess")
    async def wordle_quess(self, interaction: discord.Interaction, quess: str):
        if self.is_playing == False:
            embed = discord.Embed(
                title="", description="You need to start the game first by using **/wordle_play**", color=self.color)
            await interaction.response.send_message(embed=embed)
        else:
            self.user_quess = quess
            await interaction.response.defer(thinking=True)
            await interaction.channel.send(f"{quess}")
            await interaction.channel.purge(limit=2)

    @ app_commands.command(name="wordle_stats", description="view wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        pass


async def setup(bot):
    await bot.add_cog(Wordle(bot))
