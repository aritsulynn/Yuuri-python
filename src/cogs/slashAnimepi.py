from discord import SlashOption
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from .customFunction import anipi as ap


class slashAnipi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="anime", description="Get anime info from AniList")
    async def anime(self, interaction: Interaction, *, anime : str = SlashOption(name="anime", description="Insert anime name here!", required=True)):
        await interaction.response.defer(with_message=True,ephemeral=False)
        await interaction.followup.send(embed = ap.get_anime(anime))

    @nextcord.slash_command(name="manga", description="Get manga info from AniList")
    async def manga(self, interaction: Interaction, *, manga : str = SlashOption(name="manga", description="Insert manga name here!", required=True)):
        await interaction.response.defer(with_message=True,ephemeral=False)
        await interaction.followup.send(embed = ap.get_manga(manga))

    @nextcord.slash_command(name="user", description="Get user info from AniList")
    async def user(self, interaction: Interaction, *, user : str = SlashOption(name="username", description="Insert username here!", required=True)):
        await interaction.response.defer(with_message=True,ephemeral=False)
        await interaction.followup.send(embed = ap.get_user(user))

def setup(bot):
    bot.add_cog(slashAnipi(bot))
