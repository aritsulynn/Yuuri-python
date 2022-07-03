import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        embed = nextcord.Embed(
            title="Welcome to the server!",
            description=f"{member.mention}",
            color=0xFFA500,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(events(bot))
