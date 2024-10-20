import discord
from discord.ext import commands
import asyncio
import re

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute', help='Mute a user for a specified duration (e.g., 10s, 5m, 1h, 1d)')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, duration: str = None, *, reason=None):
        if member is None or duration is None:
            await ctx.send("Usage: `!mute @User duration reason` (e.g., `!mute @User 10m Spamming`)")
            return

        # Create a mute role if it doesn't exist
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'The user {member.mention} has been muted for {duration}! Reason: {reason}')

        # Convert duration to seconds
        seconds = self.parse_duration(duration)

        # Wait for the duration and then unmute the member
        await asyncio.sleep(seconds)
        await member.remove_roles(mute_role)
        await ctx.send(f'The user {member.mention} has been unmuted after {duration}!')

    @commands.command(name='kick', help='Kick a user from the server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'The user {member.mention} has been kicked! Reason: {reason}')

    @commands.command(name='ban', help='Ban a user from the server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'The user {member.mention} has been banned! Reason: {reason}')

    @commands.command(name='unban', help='Unban a user from the server')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_name_and_id: str):
        member_name, member_id = member_name_and_id.rsplit('#', 1)
        try:
            member = await ctx.guild.fetch_ban(discord.Object(id=int(member_id)))
            await ctx.guild.unban(member.user)
            await ctx.send(f'The user {member.user.mention} has been unbanned!')
        except Exception as e:
            await ctx.send(f'Could not unban: {e}')

    @commands.command(name='unmute', help='Unmute a user')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'The user {member.mention} has been unmuted!')

    def parse_duration(self, duration: str) -> int:
        total_seconds = 0
        pattern = re.compile(r'(\d+)([smhd])')  # Match patterns like 10s, 5m, 2h, 1d
        matches = pattern.findall(duration)

        for amount, unit in matches:
            amount = int(amount)
            if unit == 's':
                total_seconds += amount
            elif unit == 'm':
                total_seconds += amount * 60
            elif unit == 'h':
                total_seconds += amount * 3600
            elif unit == 'd':
                total_seconds += amount * 86400

        return total_seconds

async def setup(bot):
    await bot.add_cog(Moderation(bot))
