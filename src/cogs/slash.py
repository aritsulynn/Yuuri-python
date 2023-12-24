import discord 
from discord.ext import commands
from discord import app_commands


class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Commands Ready!")

    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        # await ctx.send(fmt)
        names = [command.name for command in fmt]

        await ctx.send(f"Synced {names}")

    # @app_commands.command(name="sync", description="Syncs slash commands")
    # async def sync(self, interaction: discord.Interaction):
    #     fmt = await interaction.bot.tree.sync(guild=interaction.guild)
    #     await interaction.response.send_message(fmt, ephemeral=True)

    @app_commands.command(name="ping", description="A cool ping command!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms', ephemeral=True)


async def setup(bot):
    await bot.add_cog(slash(bot), guilds=[discord.Object(id=785708140959760414)])