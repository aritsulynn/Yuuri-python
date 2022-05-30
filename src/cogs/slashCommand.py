import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import requests
from .customFunction import myFunction as mf


class slashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="rank", description="Get valorant current rank")
    async def rank(self, interaction: Interaction, *, name : str):
        await interaction.response.defer(with_message=True,ephemeral=False)
        # https://api.kyroskoh.xyz/valorant/v1/mmr/ap/ID/Tag
        names = name.split('#')
        await interaction.followup.send(requests.get(f'https://api.kyroskoh.xyz/valorant/v1/mmr/ap/{names[0]}/{names[1]}').text)
    
def setup(bot):
    bot.add_cog(slashCommands(bot))
