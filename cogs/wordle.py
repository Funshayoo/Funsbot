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
        self.letter_colors = ["<:GreenSquare:1058105080630493244>",
                              "<:YellowSquare:1058105081637122069>", "<:ColorAbsent:1058105077073711144>"]

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

        colored_word = list([self.letter_colors[2] for letter in guess])
        guess_letters = list(guess)
        answer_letters = list(answer)

        for i in range(len(guess_letters)):
            if guess_letters[i] == answer_letters[i]:
                colored_word[i] = "<:GreenSquare:1058105080630493244>"
                answer_letters[i] = None
                guess_letters[i] = None

        for i in range(len(guess_letters)):
            if guess_letters[i] is not None and guess_letters[i] in answer_letters:
                colored_word[i] = "<:YellowSquare:1058105081637122069>"
                answer_letters[i] = None
                guess_letters[i] = None

        return "".join(colored_word)

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @ app_commands.command(name="wordle", description="Play a game of wordle")
    async def wordle(self, interaction: discord.Interaction, guess: str):
        if not self.is_playing:
            await self.make_new_game()

        if await self.process_guess(guess):
            embed = discord.Embed(
                title="", description="Your guess is valid", color=self.color)
            await interaction.response.send_message(embed=embed)
        else:
            if guess == self.answer:
                embed = discord.Embed(
                    title="You won", description="", color=self.color)
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
