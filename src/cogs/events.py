import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = nextcord.Embed(
            title="Welcome to the server!",
            description=f"{member.mention}",
            color='#fff',
            thumbnail=member.avatar_url,
            timestamp=datetime.now()
        )
        await member.send(embed = embed)


def setup(bot):
    bot.add_cog(events(bot))
