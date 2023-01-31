import discord
from discord.ext import commands
from discord import app_commands

import aiosqlite
import os
from dotenv import load_dotenv

load_dotenv()
database_dir = os.getenv("DATABASE_DIRECTORY")


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded database.py!')

        async with aiosqlite.connect(database_dir) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute("CREATE TABLE IF NOT EXISTS main (user_id INTEGER, todays_word STRING, can_guess BOOLEAN, games INTEGER, wins INTEGER, losses INTEGER)")
            await wordle_db.commit()

    @app_commands.command(name="add_user", description="add user to database")
    async def add_user(self, interaction: discord.Interaction):
        user = interaction.user
        word = "apple"

        async with aiosqlite.connect(database_dir) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT user_id FROM main WHERE user_id = {user.id}")
                data = await wordle_cursor.fetchone()
                print(data)
                if data is None:
                    await wordle_cursor.execute(f"INSERT INTO main (user_id, todays_word, can_guess, games, wins, losses) VALUES {user.id, word, True, 0, 0, 0}")
            await wordle_db.commit()

        await self.bot.embed(interaction, "", title="Added user to the database")


async def setup(bot):
    await bot.add_cog(Database(bot))
