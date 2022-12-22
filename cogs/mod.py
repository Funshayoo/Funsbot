import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded mod.py!')

    # ? kick command
    @app_commands.command(name="kick", description="Kick the user")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.send_message(f'Kicked {member.mention} for reason {reason}')
        await member.kick(reason=reason)

    # ? ban command
    @app_commands.command(name="ban", description="Ban the user")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.send_message(f'Banned {member.mention} for reason {reason}')
        await member.ban(reason=reason)

    # ? mute command
    @app_commands.command(name="mute", description="Mute the user")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(reason="For what reason")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        guild = interaction.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if mutedRole:
            await member.add_roles(mutedRole, reason=reason)
            await interaction.response.send_message(f'Muted {member.mention} for reason {reason}')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')
            await member.add_roles(mutedRole, reason=reason)
            await interaction.response.send_message(f'Muted {member.mention} for reason {reason}')

    # ? unmute comand
    @app_commands.command(name="unmute", description="Unmute the user")
    @app_commands.default_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        await member.remove_roles(mutedRole)
        await interaction.response.send_message(f'Unmuted {member.mention}')

    @app_commands.command(name="clear", description="Clear the chat")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount="How much messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)

    # ? announcements command
    @app_commands.command(name="announce", description="Send a message to announcements channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(title="What title", message="What to say")
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        channel = self.client.get_channel(1053696319325229087)
        guild = interaction.guild

        if message == None:
            return
        else:
            embed = discord.Embed(
                title=title,
                description=message)
            await channel.send(embed=embed)
            await channel.send(guild.default_role)


async def setup(client):
    await client.add_cog(Mod(client))
