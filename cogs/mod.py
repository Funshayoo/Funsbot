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

    #kick command
    @app_commands.command(name="kick", description ="Kick the user")
    @has_permissions(administrator=True)
    @app_commands.describe(reason = "For what reason")
    async def kick(self, ctx, member: discord.Member, reason: str):
        await ctx.send(f'Kicked {member.mention} for reason {reason}')
        await member.kick(reason=reason)

    #ban command
    @app_commands.command(name="ban", description ="Ban the user")
    @has_permissions(administrator=True)
    @app_commands.describe(reason = "For what reason")
    async def ban(self, ctx, member: discord.Member, reason: str):
        await ctx.send(f'Banned {member.mention} for reason {reason}')
        await member.ban(reason=reason)

    #mute command
    @app_commands.command(name="mute", description ="Mute the user")
    @has_permissions(administrator=True)
    @app_commands.describe(reason = "For what reason")
    async def mute(self, ctx, member: discord.Member, reason: str):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if mutedRole:
            await member.add_roles(mutedRole, reason=reason)
            await ctx.send(f'Muted {member.mention} for reason {reason}')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')
            await member.add_roles(mutedRole, reason=reason)
            await ctx.send(f'Muted {member.mention} for reason {reason}')

    #unmute comand
    @app_commands.command(name="unmute", description ="Unmute the user")
    @has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        await member.remove_roles(mutedRole)
        await ctx.send(f'Unmuted {member.mention}')


    @app_commands.command(name="clear", description ="Clear the chat")
    @has_permissions(administrator=True)
    @app_commands.describe(amount = "How much messages")
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    #announcements command
    @app_commands.command(name="announce", description ="Send a message to announcements channel")
    @has_permissions(administrator=True)
    @app_commands.describe(message = "What to say")
    async def announce(self, ctx, message: str):
        channel = self.client.get_channel(1008123488755793980)

        if message == None:
            return
        else:
            embed = discord.Embed(
        title='Ważna informacja!',
        description=message)
        await channel.send(embed=embed)
        await channel.send(ctx.message.guild.default_role)

async def setup(client):
    await client.add_cog(Mod(client))
