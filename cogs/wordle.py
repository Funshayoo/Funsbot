import discord
from discord.ext import commands
from discord import app_commands

import random
import datetime
import csv


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color
        self.is_playing = False
        self.answer = ""
        self.letter_colors = ["<:GreenSquare:1058105080630493244>",
                              "<:YellowSquare:1058105081637122069>", "<:ColorAbsent:1058105077073711144>"]

        # * all word dictionaries
        self.popular = open(
            "./wordle_src/wordle_words.txt").read().splitlines()
        self.all_words = set(word.strip()
                             for word in open("./wordle_src/dictionary.txt"))

    async def get_random_word(self) -> str:
        return random.choice(self.popular)

    async def make_new_game(self) -> None:
        self.is_playing = True
        self.answer = await self.get_random_word()
        print(self.answer)

    async def process_guess(self, word: str) -> bool:
        word = word.lower()
        if word in self.all_words:
            self.user_guess = word
            valid = True
        else:
            valid = False

        return valid

    async def generate_colored_word(self, guess: str, answer: str) -> str:

        colored_word = list([self.letter_colors[2] for letter in guess])
        guess_letters = list(guess)
        answer_letters = list(answer)

        for i in range(len(guess_letters)):
            if guess_letters[i] == answer_letters[i]:
                colored_word[i] = self.letter_colors[0]
                answer_letters[i] = None
                guess_letters[i] = None

        for i in range(len(guess_letters)):
            if guess_letters[i] is not None and guess_letters[i] in answer_letters:
                colored_word[i] = self.letter_colors[1]
                answer_letters[answer_letters.index(guess_letters[i])] = None

        return "".join(colored_word)

    async def played_today(self) -> bool:
        pass

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    @ app_commands.command(name="wordle", description="Play a game of wordle")
    @app_commands.describe(guess="Your guess")
    async def wordle(self, interaction: discord.Interaction,  guess: str):
        if not self.is_playing:
            await self.make_new_game()

        if not await self.process_guess(guess):
            await self.bot.embed(interaction, "Your guess is invalid", ephemeral=True)
        else:
            if guess == self.answer:
                self.is_playing = False
                await self.bot.embed(interaction, f"The answer was: **{self.answer}**", title=f"{interaction.user} guessed the word!")
            else:
                colored_word = await self.generate_colored_word(guess, self.answer)
                await self.bot.embed(interaction, f"{colored_word} {guess}")

    @ app_commands.command(name="wordle_stats", description="View your wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "", title="Comming soon :eyes:")


async def setup(bot):
    await bot.add_cog(Wordle(bot))
