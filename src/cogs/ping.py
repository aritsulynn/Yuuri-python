import discord
from discord.ext import commands
from datetime import datetime

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        print("ping")
        await ctx.reply("hello")

    @commands.command()
    async def profile(self, ctx):
        embed = discord.Embed(title="Profile", description="This is a test", color=0x00ff00)
        embed.add_field(name="Name", value="Value", inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ping(bot))