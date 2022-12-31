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
        self.letter_colors = {
            "green": "<:GreenSquare:1058105080630493244>",
            "yellow": "<:YellowSquare:1058105081637122069>",
            "grey": "<:ColorAbsent:1058105077073711144>",
            "blank": ":white_medium_square:"
        }

        # * all word dictionaries
        self.popular = open(
            "./wordle_src/wordle_words.txt").read().splitlines()
        self.all_words = open(
            "./wordle_src/dictionary.txt").read().splitlines()

    async def get_random_word(self) -> str:
        return random.choice(self.popular)

    async def make_new_game(self) -> None:
        self.is_playing = True
        self.answer = await self.get_random_word()
        print(self.answer)

    async def generate_blanks(self) -> str:
        return ((self.letter_colors["blank"] * 5) + ("\n")) * 6

    async def process_guess(self, word: str) -> bool:
        word = word.lower()
        if word in self.all_words:
            self.user_guess = word
            valid = False
        else:
            valid = True

        return valid

    # TODO finish this function
    async def generate_colored_word(self, guess: str, answer: str) -> str:

        colored_word = self.letter_colors["grey"] * len(guess)
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

        return "".join(colored_word)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @app_commands.command(name="wordle", description="Play a game of wordle")
    async def wordle(self, interaction: discord.Interaction, guess: str):
        if not self.is_playing:
            await self.make_new_game()
            # blanks = await self.generate_blanks()
            # embed = discord.Embed(title="",
            #                       description=f"{blanks}", color=self.color)
            # await interaction.response.send_message(embed=embed)``

        if await self.process_guess(guess):
            embed = discord.Embed(
                title="", description="Your guess is valid", color=self.color)
            await interaction.response.send_message(embed=embed)
        else:
            colored_word = await self.generate_colored_word(guess, self.answer)
            embed = discord.Embed(
                title="", description=f"{colored_word} {guess}", color=self.color)
            await interaction.response.send_message(embed=embed)

    @ app_commands.command(name="wordle_stats", description="view your wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        pass


async def setup(bot):
    await bot.add_cog(Wordle(bot))
