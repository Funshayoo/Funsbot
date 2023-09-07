import discord
from discord.ext import commands
from discord import app_commands

import random
import aiosqlite
from config import Config


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.answer = ""
        self.tries_left = 0

        self.letter_colors = {"green": "<:green:1149418205027238038>",
                              "yellow": "<:yellow:1149418215831777390>", "grey": "<:grey:1149418192297537596>"}

        self.all_words = set(word.strip()
                             for word in open("./wordle_src/dictionary.txt"))

    def get_random_word(self) -> str:
        return random.choice(open("./wordle_src/wordle_words.txt").read().splitlines())

    async def make_new_game(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        self.answer = self.get_random_word()
        print(self.answer)

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT answer, tries_left, game_started, games_played FROM wordle WHERE user_id = {user.id}")
                user_data = await wordle_cursor.fetchone()
                games_played = user_data[3]

                sql = (
                    "UPDATE wordle SET answer = ?, tries_left = ?, game_started = ?, games_played = ? WHERE user_id = ?")
                val = (self.answer, 5, True, games_played + 1, user.id)
                await wordle_cursor.execute(sql, val)
            await wordle_db.commit()

    def guess_valid(self, word: str) -> bool:
        return word.lower() in self.all_words

    def generate_colored_word(self, guess: str, answer: str) -> str:

        colored_word = list([self.letter_colors["grey"] for letter in guess])
        guess_letters = list(guess)
        answer_letters = list(answer)

        for i in range(len(guess_letters)):
            if guess_letters[i] == answer_letters[i]:
                colored_word[i] = self.letter_colors["green"]
                answer_letters[i] = None
                guess_letters[i] = None

        for i in range(len(guess_letters)):
            if guess_letters[i] is not None and guess_letters[i] in answer_letters:
                colored_word[i] = self.letter_colors["yellow"]
                answer_letters[answer_letters.index(guess_letters[i])] = None

        return "".join(colored_word)

    async def user_won(self, interaction: discord.Interaction) -> bool:
        user = interaction.user
        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT wins FROM wordle WHERE user_id = {user.id}")

                user_data = await wordle_cursor.fetchone()
                wins = user_data[0]
                sql = (
                    "UPDATE wordle SET wins = ?, game_started = ?, answer = ?, tries_left = ? WHERE user_id = ?")
                val = (wins + 1, False, "", 5, user.id)
                await wordle_cursor.execute(sql, val)

            await wordle_db.commit()
        await self.bot.embed(interaction, f"The answer was: **{self.answer}**", title=f"{interaction.user} guessed the word!", followup=True)

    async def remove_try(self, interaction):
        user = interaction.user
        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT tries_left FROM wordle WHERE user_id = {user.id}")

                user_data = await wordle_cursor.fetchone()
                tries_left = user_data[0]
                self.tries_left = tries_left - 1
                sql = (
                    "UPDATE wordle SET tries_left = ? WHERE user_id = ?")
                val = (self.tries_left, user.id)
                await wordle_cursor.execute(sql, val)

            await wordle_db.commit()

    async def game_over(self, interaction):
        user = interaction.user
        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT losses FROM wordle WHERE user_id = {user.id}")

                user_data = await wordle_cursor.fetchone()
                losses = user_data[0]
                sql = (
                    "UPDATE wordle SET losses = ?, game_started = ?, answer = ?, tries_left = ? WHERE user_id = ?")
                val = (losses + 1, False, "", 5, user.id)
                await wordle_cursor.execute(sql, val)

            await wordle_db.commit()
        await self.bot.embed(interaction, f"The answer was: {self.answer}", "Game over:", followup=True)

    @ commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    @ app_commands.command(name="wordle", description="Play a game of wordle")
    @ app_commands.describe(guess="Your guess")
    async def wordle(self, interaction: discord.Interaction, guess: str):
        user = interaction.user

        await interaction.response.defer()

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT game_started, answer, tries_left FROM wordle WHERE user_id = {user.id}")

                user_data = await wordle_cursor.fetchone()
                self.is_playing = user_data[0]
                self.answer = user_data[1]
                self.tries_left = user_data[2]

            await wordle_db.commit()

        if not self.is_playing:
            await self.make_new_game(interaction)

        if not self.guess_valid(guess):
            await self.bot.embed(interaction, "Your guess is invalid", ephemeral=True, followup=True)
        else:
            if guess == self.answer:
                await self.user_won(interaction)
            elif self.tries_left <= 1:
                await self.game_over(interaction)
            else:
                await self.remove_try(interaction)
                colored_word = self.generate_colored_word(guess, self.answer)
                await self.bot.embed(interaction, f"{colored_word} {guess}", title="Your guess:", footer=f"tries left: {self.tries_left}", followup=True)

    @ app_commands.command(name="wordle_stats", description="View your wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        user = interaction.user

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT games_played, wins, losses FROM wordle WHERE user_id = {user.id}")
                stats = await wordle_cursor.fetchone()
                try:
                    games_played = stats[0]
                    wins = stats[1]
                    losses = stats[2]
                except Exception:
                    games_played = 0
                    wins = 0
                    losses = 0

            await wordle_db.commit()

        if games_played == 0:
            await self.bot.embed(interaction, 'You need to play some games_played first', ephemeral=True)
        else:
            if wins == 0:
                win_ratio = 0
            else:
                win_ratio = round(100 * wins / games_played)

            await self.bot.embed(interaction, f"Games: {games_played} \n Wins: {wins} \n Losses: {losses}\n Win ratio: {win_ratio}%", title="Your score:")


async def setup(bot):
    await bot.add_cog(Wordle(bot))
