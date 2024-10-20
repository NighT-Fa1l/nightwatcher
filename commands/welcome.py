from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1297460762989826102  # Replace with your channel ID

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(f'Welcome to the server, {member.mention}! 🎉')

async def setup(bot):
    await bot.add_cog(Welcome(bot))
