import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import List, Optional


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color
        self.is_playing = False
        self.answer = ""
        self.user_guess = ""
        self.letters_colors = {
            "green": "<:GreenSquare:1058105080630493244>",
            "yellow": "<:YellowSquare:1058105081637122069>",
            "grey": "<:ColorAbsent:1058105077073711144>"
        }

        # * all word dictionaries
        self.popular = open(
            "./wordle_src/wordle_words.txt").read().splitlines()
        self.all_words = open(
            "./wordle_src/dictionary.txt").read().splitlines()

    async def get_random_word(self) -> str:
        wordle_word = self.popular
        return random.choice(wordle_word)

    async def generate_blanks(self) -> str:
        return (("<:EmptySquare:1058105078709506168>" * 5) + ("\n")) * 6

    async def is_word_valid(self, word: str) -> bool:
        valid = False
        if word in self.all_words:
            valid = False
            return valid
        else:
            valid = True
            return valid

    async def generate_colored_word(self, guess: str, answer: str) -> str:

        # colored_word = "0" * len(guess)
        # guess_letters: List[Optional[str]] = list(guess)
        # answer_letters: List[Optional[str]] = list(answer)

        # for i in range(len(guess)):
        # for i in range(len(guess_letters)):
        #     if guess_letters[i] == answer_letters[i]:
        #         colored_word[i] = self.letters_colors["green"]
        #         answer_letters[i] = None
        #         guess_letters[i] = None

        # for i in range(len(guess)):
        #     if guess[i] is not None and guess[i] in answer:
        #         colored_word[i] = self.letters_colors["yellow"]
        #         answer[answer.index(guess[i])] = None

        return "".join(answer)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @app_commands.command(name="wordle_play", description="Play a game of wordle")
    async def play_wordle(self, interaction: discord.Interaction):
        if self.is_playing:
            embed = discord.Embed(
                title="", description="Game has already started", color=self.color)
            await interaction.response.send_message(
                embed=embed, ephemeral=True)
        else:
            self.is_playing = True
            self.is_playing = True
            self.answer = await self.get_random_word()
            blanks = await self.generate_blanks()
            embed = discord.Embed(title="Guees the word using: **/wordle_guess**",
                                  description=f"{blanks}", color=self.color)
            await interaction.response.send_message(embed=embed)
            print(self.answer)

    @ app_commands.command(name="wordle_guess", description="Guess a word")
    @ app_commands.describe(guess="Your guess")
    async def wordle_guess(self, interaction: discord.Interaction, guess: str):
        if self.is_playing == False:
            embed = discord.Embed(
                title="", description="You need to start the game first by using **/wordle_play**", color=self.color)
            await interaction.response.send_message(embed=embed)
        else:
            word_valid = await self.is_word_valid(guess.lower())
            if word_valid == False:
                self.user_guess = guess.lower()
                await interaction.response.defer(thinking=True)
                await interaction.channel.send(f"{guess}")
                await interaction.channel.purge(limit=2)
                color_word = await self.generate_colored_word(self.user_guess, self.answer)
                await interaction.channel.send(f"{color_word}")
            else:
                embed = discord.Embed(
                    title="", description="Your word is not in the dictionary", color=self.color)
                await interaction.response.send_message(embed=embed)

    @ app_commands.command(name="wordle_stats", description="view your wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        pass


async def setup(bot):
    await bot.add_cog(Wordle(bot))
