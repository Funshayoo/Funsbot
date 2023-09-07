import discord
from discord.ext import commands
from discord import app_commands


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

    @app_commands.command(name="odkurzacz", description="wyczysc czat")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount="ilosc wiadomosci")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(thinking=True)
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="", description=f'Usunieto {amount} wiadomosci)', color=self.self.bot.embed_color)
        await interaction.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Cmds(bot))
