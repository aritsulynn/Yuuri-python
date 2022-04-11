import nextcord
from nextcord import Interaction
from nextcord.ext import commands

# from .customFunction import myFunction as mf
from .customFunction import anipi as ap


class slashAnipi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="anime", description="Get anime info from AniList")
    async def anilist(self, interaction: Interaction, *, anime : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ap.get_anime(anime))


    @nextcord.slash_command(name="manga", description="Get manga info from AniList")
    async def manga(self, interaction: Interaction, *, manga : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ap.get_manga(manga))


    @nextcord.slash_command(name="user", description="Get user info from AniList")
    async def user(self, interaction: Interaction, *, user : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ap.get_user(user))


def setup(bot):
    bot.add_cog(slashAnipi(bot))
