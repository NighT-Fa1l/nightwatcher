from discord.ext import commands
import datetime
import asyncio
import discord  # Don't forget to import discord for role checks

class FriendGreet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_greeted = {}
        self.role_id = 1297306150278004796  # Replace with your specific role ID

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the author has the specific role
        role = discord.utils.get(message.guild.roles, id=self.role_id)
        if role in message.author.roles:
            now = datetime.datetime.now()
            user_id = message.author.id
            
            # Debugging print statement
            print(f"Message from {message.author}: {message.content}")

            # Check if the user has been greeted in the last hour
            if user_id not in self.last_greeted or (now - self.last_greeted[user_id]).total_seconds() >= 3600:
                self.last_greeted[user_id] = now  # Update the last greeted time
                await message.reply('hello NighTs friend [hehe](https://cdn.discordapp.com/emojis/977619327811465276.webp?size=48&quality=lossless&name=CreepySmile)')

            # To keep the greeting going every hour after the first message:
            await self.send_periodic_greetings(user_id, message.channel)

    async def send_periodic_greetings(self, user_id, channel):
        while True:
            await asyncio.sleep(3600)  # Wait for one hour
            now = datetime.datetime.now()
            if user_id in self.last_greeted and (now - self.last_greeted[user_id]).total_seconds() >= 3600:
                self.last_greeted[user_id] = now  # Update the last greeted time
                # Send the greeting to the same channel
                await channel.send(f'I been watching the server for you when you were away [hehe](https://cdn.discordapp.com/emojis/977619327811465276.webp?size=48&quality=lossless&name=CreepySmile)')

async def setup(bot):
    await bot.add_cog(FriendGreet(bot))
