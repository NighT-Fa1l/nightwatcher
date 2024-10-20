from discord.ext import commands
import datetime
import asyncio

class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_greeted = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Replace with your Discord user ID
        if message.author.id == 831032738362425375:  # Replace with your actual user ID
            now = datetime.datetime.now()
            user_id = message.author.id
            
            # Debugging print statement
            print(f"Message from {message.author}: {message.content}")

            # Check if the user has been greeted in the last hour
            if user_id not in self.last_greeted or (now - self.last_greeted[user_id]).total_seconds() >= 3600:
                self.last_greeted[user_id] = now  # Update the last greeted time
                await message.reply('I been watching the server for you when you were away [hehe](https://cdn.discordapp.com/emojis/977619327811465276.webp?size=48&quality=lossless&name=CreepySmile)')

            # To keep the greeting going every hour after the first message:
            await self.send_periodic_greetings(user_id)

    async def send_periodic_greetings(self, user_id):
        while True:
            await asyncio.sleep(3600)  # Wait for one hour
            now = datetime.datetime.now()
            if user_id in self.last_greeted and (now - self.last_greeted[user_id]).total_seconds() >= 3600:
                self.last_greeted[user_id] = now  # Update the last greeted time
                # Send the greeting to the channel where the user last messaged
                channel = self.bot.get_channel(user_id)  # Get the channel (might need adjustment)
                if channel:
                    await channel.send(f'I been watching the server for you when you were away [hehe](https://cdn.discordapp.com/emojis/977619327811465276.webp?size=48&quality=lossless&name=CreepySmile)')

async def setup(bot):
    await bot.add_cog(Greet(bot))
