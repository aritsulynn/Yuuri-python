from discord import SlashOption
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import requests
from .customFunction import myFunction as mf


class slashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="rank", description="Get valorant current rank")
    async def rank(self, interaction: Interaction, *, name : str = SlashOption(name='name', description='Insert your game name.', required=True), tag : str = SlashOption(name='tag', description='Insert your tag.', required=True)):
        await interaction.response.defer(with_message=True,ephemeral=False)
        # https://api.kyroskoh.xyz/valorant/v1/mmr/ap/ID/Tag
        await interaction.followup.send(f'{name}#{tag} is ' + requests.get(f'https://api.kyroskoh.xyz/valorant/v1/mmr/ap/{name}/{tag}').text)
    
def setup(bot):
    bot.add_cog(slashCommands(bot))
