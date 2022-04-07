import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from . import myFunction as mf


class slashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="search")
    async def search(self, interaction: Interaction):
        pass
    
    @search.subcommand()
    async def anime(self, interaction: Interaction):
        pass

    @search.subcommand()
    async def manga(self, interaction: Interaction):
        pass

    @anime.subcommand(name="search")
    async def ani_search(self, interaction: Interaction, *, username):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = mf.ani_search(username , "all"))

    @anime.subcommand(name="watching")
    async def ani_watching(self, interaction: Interaction, *, username):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = mf.ani_search(username, "watching"))
    
    @anime.subcommand(name="completed")
    async def ani_completed(self, interaction: Interaction, *, username):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = mf.ani_search(username, "Completed"))

    # @manga.subcommand(name="search")
    # async def mg_search(self, interaction: Interaction, *, username):
    #     await interaction.response.defer(with_message=True,ephemeral=True)
    #     await interaction.followup.send(embed = mf.mg_search(username , "all"))
    
    # @manga.subcommand(name="reading")
    # async def mg_reading(self, interaction: Interaction, *, username):
    #     await interaction.response.defer(with_message=True,ephemeral=True)
    #     await interaction.followup.send(embed = mf.mg_search(username, "reading"))
    
    # @manga.subcommand(name="completed")
    # async def mg_completed(self, interaction: Interaction, *, username):
    #     await interaction.response.defer(with_message=True,ephemeral=True)
    #     await interaction.followup.send(embed = mf.mg_search(username, "Completed"))


def setup(bot):
    bot.add_cog(slashCommands(bot))
