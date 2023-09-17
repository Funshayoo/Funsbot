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
    async def pomoc(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, '''

        `/pomoc` - ta komenda
        `/odkurzacz` - (komenda tylko dla adminow) wyczysc czat
        `/moneta` - rzut moneta
        `/zarcik` - zarcik kosmonaucik
        `/zadania` - zobacz zapowiedziane zadania na jutro
        `/play` - pusc muzyke
        `/pause_resume` - zatrzymaj/wznow muzyke
        `/skip` - pomin utwor
        `/queue` - wyswietl kolejke
        `/queue_clear` - wyczysc kolejke
        `/leave` - wywal bota z vc
        `/nowplaying` - wyswietl tytyl teraz odtwarzanego utworu
        `/loop` - zapetl utwor
        `/wordle` - zagraj w wordle
        `/wordle_stats` - wyswietl twoje statystyki w wordle

        ''', title="/**nazwa_komendy**", ephemeral=True)

    @app_commands.command(name="odkurzacz", description="wyczysc czat")
    @app_commands.describe(amount="ilosc wiadomosci do usuniecia")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def odkurzacz(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(thinking=True)
        await interaction.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title="", description=f'Usunieto {amount} wiadomosci)', color=self.self.bot.embed_color)
        await interaction.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Cmds(bot))
