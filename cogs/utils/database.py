import aiosqlite
from config import Config


class Database:

    async def db_connect(self):
        db = await aiosqlite.connect(Config.DATABASE_DIRECTORY)
        db.row_factory = aiosqlite.Row
        return db

    async def db_execute(self, sql, val=None):
        db = await self.db_connect()
        cursor = await db.cursor()
        await cursor.execute(sql)
        await db.commit()
        await db.close()

    async def db_create(self):
        sql = "CREATE TABLE IF NOT EXISTS wordle (user_id INTEGER, answer STRING, tries_left INTEGER, game_started BOOLEAN, games_played INTEGER, wins INTEGER, losses INTEGER)"
        await self.db_execute(sql)
