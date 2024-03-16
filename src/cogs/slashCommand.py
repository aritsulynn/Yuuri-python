import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()




class slashCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Commands Ready!")

    @app_commands.command(name="ping", description="A cool ping command!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True
        )

    @app_commands.command(name="profile", description="A cool profile command!")
    async def profile(self, interaction: discord.Interaction):
        """A cool profile command!"""
        embed = discord.Embed(
            title="Profile",
            description="This is a profile command!",
            color=discord.Color.random(),
        )


async def setup(bot):
    await bot.add_cog(
        slashCommand(bot),
        guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
    )
