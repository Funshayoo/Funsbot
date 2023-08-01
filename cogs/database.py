import discord
from discord.ext import commands
from discord import app_commands

import aiosqlite
from config import Config


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded database.py!')

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute("CREATE TABLE IF NOT EXISTS wordle (user_id INTEGER, answer STRING, tries_left INTEGER, game_started BOOLEAN, games_played INTEGER, wins INTEGER, losses INTEGER)")
            await wordle_db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        user = message.author

        async with aiosqlite.connect(Config.DATABASE_DIRECTORY) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute(f"SELECT user_id FROM wordle WHERE user_id = {user.id}")
                data = await wordle_cursor.fetchone()
                if data is None:
                    sql = (
                        "INSERT INTO wordle (user_id, answer, tries_left, game_started, games_played, wins, losses) VALUES (?, ?, ?, ?, ?, ?, ?)")
                    val = (user.id, "", 5, False, 0, 0, 0)
                    await wordle_cursor.execute(sql, val)
            await wordle_db.commit()


async def setup(bot):
    await bot.add_cog(Database(bot))
