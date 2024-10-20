import discord
from discord.ext import commands
import random
import json

class LevelingSystem:
    def __init__(self, filename='xp_data.json'):
        self.filename = filename
        self.xp_data = self.load_xp_data()

    def load_xp_data(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_xp_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.xp_data, f)

    async def add_xp(self, user_id, amount, bot):
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {'xp': 0, 'level': 1}

        self.xp_data[user_id]['xp'] += amount
        level = self.xp_data[user_id]['level']
        required_xp = 100 * (2 ** (level - 1))  # XP required for the current level

        # Check for level up
        while self.xp_data[user_id]['xp'] >= required_xp:
            self.xp_data[user_id]['level'] += 1
            level += 1
            required_xp = 100 * (2 ** (level - 1))  # Update required XP for the new level
            channel = bot.get_channel(1297692455856111716)  # Replace with your channel ID
            if channel:
                new_level = self.xp_data[user_id]['level']
                await channel.send(
                    embed=discord.Embed(
                        title="🎉 Level Up! 🎉",
                        description=f"Congratulations, {bot.get_user(user_id).mention}! You've reached level **{new_level}**!",
                        color=discord.Color.from_rgb(243, 244, 245)  # Using the specified color
                    )
                )

        self.save_xp_data()

    def get_user_data(self, user_id):
        return self.xp_data.get(user_id, {'xp': 0, 'level': 0})

class Levelup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leveling_system = LevelingSystem()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Add random XP for every message sent
        await self.leveling_system.add_xp(message.author.id, random.randint(10, 50), self.bot)

    @commands.command()
    async def level(self, ctx):
        """Check your current level and XP."""
        user_id = ctx.author.id
        user_data = self.leveling_system.get_user_data(user_id)
        xp = user_data['xp']
        level = user_data['level']
        
        # Create an embed for the response with the specified color
        embed = discord.Embed(
            title="Server Level Info!",
            description=f"{ctx.author.mention}, your level is **{level}**.",
            color=discord.Color.from_rgb(243, 244, 245)  # Using the specified color
        )
        embed.add_field(name="XP", value=f"{xp} XP", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levelup(bot))
