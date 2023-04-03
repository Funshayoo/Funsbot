import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions

import asyncio


class Cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded cmds.py!')

    # ? help command
    @app_commands.command(name="help", description="use this command to get some help")
    async def help(self, interaction: discord.Interaction):
        await self.bot.embed(interaction, "You can use commands by typing /**command**", ephemeral=True)

    # ? kick command
    @app_commands.command(name="kick", description="Kick the user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await self.bot.embed(interaction, f'Kicked {member.mention} for reason {reason}')
        await member.kick(reason=reason)

    # ? ban command
    @app_commands.command(name="ban", description="Ban the user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await self.bot.embed(interaction, f'Banned {member.mention} for reason {reason}')
        await member.ban(reason=reason)

    # ? mute command
    @app_commands.command(name="mute", description="Mute the user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        guild = interaction.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')
        await self.bot.embed(interaction, f'Muted {member.mention} for reason {reason}')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

        await member.add_roles(mutedRole, reason=reason)

    # ? unmute command
    @app_commands.command(name="unmute", description="Unmute the user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')
        await self.bot.embed(interaction, f'Unmuted {member.mention}')
        await member.remove_roles(mutedRole)

    @app_commands.command(name="clear", description="Clear the chat")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount="How much messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(thinking=True)
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="", description=f'Cleared {amount} message(s)', color=self.self.bot.embed_color)
        await interaction.channel.send(embed=embed)

    # ? announcements command
    @app_commands.command(name="announce", description="Send a message to announcements channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(title="What title", message="What to say")
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        channel = self.bot.get_channel(1053696319325229087)
        guild = interaction.guild

        if message == None:
            return
        else:
            embed = discord.Embed(
                title=title, description=message, color=self.bot.embed_color)
            await channel.send(embed=embed)
            await channel.send(guild.default_role)


async def setup(bot):
    await bot.add_cog(Cmds(bot))
