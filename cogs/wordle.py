import discord
from discord.ext import commands
from discord import app_commands

import random
import datetime
import aiosqlite
from config import Config


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

    def get_random_word(self) -> str:
        return random.choice(self.popular)

    async def make_new_game(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        self.answer = self.get_random_word()
        print(self.answer)

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT todays_word, tries, game_started, games FROM wordle WHERE user_id = {user.id}")
                user_data = await wordle_cursor.fetchone()
                games = user_data[3]

                sql = (
                    "UPDATE wordle SET todays_word = ?, tries = ?, game_started = ?, games = ? WHERE user_id = ?")
                val = (self.answer, 5, True, games + 1, user.id)
                await wordle_cursor.execute(sql, val)
            await wordle_db.commit()

    def process_guess(self, word: str) -> bool:
        word = word.lower()
        if word in self.all_words:
            self.user_guess = word
            valid = True
        else:
            valid = False

        return valid

    def generate_colored_word(self, guess: str, answer: str) -> str:

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

    async def user_won(self, interaction: discord.Interaction) -> bool:
        # user = interaction.user
        # async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
        #     async with wordle_db.cursor() as wordle_cursor:
        #         await wordle_cursor.execute(f"SELECT game_started, wins FROM wordle WHERE user_id = {user.id}")

        #         user_data = await wordle_cursor.fetchone()
        #         wins = user_data[1]
        #         sql = (
        #             "UPDATE wordle SET game_started = ?, wins = ? WHERE user_id = ?")
        #         val = (False, wins + 1)
        #         await wordle_cursor.execute(sql, val)

        #     await wordle_db.commit()
        await self.bot.embed(interaction, f"The answer was: **{self.answer}**", title=f"{interaction.user} guessed the word!")

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    @ app_commands.command(name="wordle", description="Play a game of wordle")
    @ app_commands.describe(guess="Your guess")
    async def wordle(self, interaction: discord.Interaction,  guess: str):
        user = interaction.user

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT game_started, todays_word FROM wordle WHERE user_id = {user.id}")

                user_data = await wordle_cursor.fetchone()
                self.is_playing = user_data[0]
                self.answer = user_data[1]

            await wordle_db.commit()

        if self.is_playing == False:
            await self.make_new_game(interaction)

        if not self.process_guess(guess):
            await self.bot.embed(interaction, "Your guess is invalid", ephemeral=True)
        else:
            if guess == self.answer:
                await self.user_won(interaction)

            else:
                colored_word = self.generate_colored_word(guess, self.answer)
                await self.bot.embed(interaction, f"{colored_word} {guess}")

    @ app_commands.command(name="wordle_stats", description="View your wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        user = interaction.user

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT games, wins, losses FROM wordle WHERE user_id = {user.id}")
                stats = await wordle_cursor.fetchone()
                try:
                    games = stats[0]
                    wins = stats[1]
                    losses = stats[2]
                except:
                    games = 0
                    wins = 0
                    losses = 0

            await wordle_db.commit()

        if games == 0:
            await self.bot.embed(interaction, 'You need to play some games first', ephemeral=True)
        else:
            if wins == 0:
                win_ratio = 0
            else:
                win_ratio = games / wins * 100

            await self.bot.embed(interaction, f"Games: {games} \n Wins: {wins} \n Losses: {losses}\n Win ratio: {win_ratio}%", title="Your score:")


async def setup(bot):
    await bot.add_cog(Wordle(bot))
