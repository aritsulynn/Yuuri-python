import nextcord
from nextcord import Interaction
from nextcord.ext import commands


from .customFunction import anisearch as ani

class slashAnilist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="anime", description="Search for an anime")
    async def anime(self, interaction: Interaction):
        pass

    @nextcord.slash_command(name="manga", description="Search for a manga")
    async def manga(self, interaction: Interaction):
        pass
    
    @anime.subcommand(name="all", description="Search for an anime")
    async def ani_all(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "all"))

    @anime.subcommand(name="watching", description="Search for an anime you are watching")
    async def ani_watching(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "watching"))
    
    @anime.subcommand(name="completed", description="Search for completed anime")
    async def ani_completed(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "completed"))

    @anime.subcommand(name="paused", description="Search for an anime that is paused")
    async def ani_paused(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "paused"))

    @anime.subcommand(name="dropped", description="Search for anime you have dropped")
    async def ani_dropped(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "dropped"))

    @anime.subcommand(name="planning" , description="Search for an anime in your planning list")
    async def ani_planning(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "anime", "planning"))


    # manga 
    @manga.subcommand(name="all", description="Search for a manga")
    async def manga_all(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "manga", "all"))
    
    @manga.subcommand(name="reading", description="Search for a manga you are reading")
    async def manga_reading(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        await interaction.followup.send(embed = ani.ani_search(username, "manga", "reading"))
    
    @manga.subcommand(name="completed", description="Search for completed manga")
    async def manga_completed(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        try:
            await interaction.followup.send(embed = ani.ani_search(username, "manga", "completed"))
        except:
            await interaction.followup.send("No completed manga found")
    
    @manga.subcommand(name="paused", description="Search for a manga you have on hold")
    async def manga_paused(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        try:
            await interaction.followup.send(embed = ani.ani_search(username, "manga", "paused"))
        except:
            await interaction.followup.send("No manga on hold found")
    
    @manga.subcommand(name="planning", description="Search for a manga you have planning")
    async def manga_planning(self, interaction: Interaction, *, username : str):
        await interaction.response.defer(with_message=True,ephemeral=True)
        try:
            await interaction.followup.send(embed = ani.ani_search(username, "manga", "planning"))
        except:
            await interaction.followup.send("No manga found")

def setup(bot):
    bot.add_cog(slashAnilist(bot))
