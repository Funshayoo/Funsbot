import discord
from discord.ext import commands
from discord import app_commands
from config import Config


class Cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded cmds.py!')

    # ? help command
    @app_commands.command(name="pomoc", description="potrzebna pomoc")
    async def help(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "/**komenda**", ephemeral=True)

    @app_commands.command(name="clear", description="Clear the chat")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount="ammount of messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(thinking=True)
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="", description=f'Cleared {amount} message(s)', color=self.self.bot.embed_color)
        await interaction.channel.send(embed=embed)

    # ? announcements command
    @app_commands.command(name="info", description="dodaj ogloszenie")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(title="tytul", message="wiadomosc")
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        channel = self.bot.get_channel(Config.DISCORD_ANNOUNCEMENT_CHANNEL)
        guild = interaction.guild

        if message is None:
            return
        else:
            embed = discord.Embed(
                title=title, description=message, color=self.bot.embed_color)
            await channel.send(embed=embed)
            await channel.send(guild.default_role)


async def setup(bot):
    await bot.add_cog(Cmds(bot))
