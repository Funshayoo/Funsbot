import discord
from discord.ext import commands
from discord import app_commands

import sqlite3
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
        wordle_database = sqlite3.connect(
            database_dir)
        wordle_cursor = wordle_database.cursor()
        wordle_cursor.execute('''CREATE TABLE IF NOT EXISTS main (
            user_id INTEGER)''')

    @app_commands.command(name="test_database", description="test the database")
    async def test_database(self, interaction: discord.Interaction):
        wordle_database = sqlite3.connect(
            database_dir)
        wordle_cursor = wordle_database.cursor()
        author = interaction.user
        wordle_cursor.execute(
            f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = wordle_cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(user_id) VALUES (?)")
            val = (author.id)
            wordle_cursor.execute(sql, val)
        wordle_database.commit()
        wordle_cursor.close()
        wordle_database.close()
        await self.bot.embed(interaction, "Test")


async def setup(bot):
    await bot.add_cog(Database(bot))
