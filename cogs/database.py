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
                await wordle_cursor.execute("CREATE TABLE IF NOT EXISTS main (user_id INTEGER, guild_id INTEGER)")
            await wordle_db.commit()

    async def test_database(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        async with aiosqlite.connect(database_dir) as wordle_db:
            async with wordle_db.cursor() as wordle_cursor:
                await wordle_cursor.execute("SELECT user_id FROM main WHERE guild_id = ?", (guild.id,))
                data = await wordle_cursor.fetchone()
                if data:
                    await wordle_cursor.execute("UPDATE main SET id = ? WHERE guild_id = ?", (user.id, guild.id))
                else:
                    await wordle_cursor.execute("INSERT INTO main (user_id, guild_id) VALUES (?, ?)", (user.id, guild.id))
            await wordle_db.commit()


async def setup(bot):
    await bot.add_cog(Database(bot))
