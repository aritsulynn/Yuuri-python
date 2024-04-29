import os
import discord
from discord.ext import commands
from datetime import datetime


class nmCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        print("ping")
        await ctx.reply("hello")

    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        # await ctx.send(fmt)
        names = [command.name for command in fmt]
        await ctx.send(f"Synced {names}")

    @commands.command()
    async def desync(self, ctx):
        self.bot.tree.clear_commands(guild=ctx.guild)
        await self.bot.tree.sync()
        await ctx.send("Desynced")

    # @commands.command()
    # async def ask(self, ctx, *, prompt):
    #     """Ask AI command!"""
    #     # Get or create a chat instance for the context
    #     chat = self.get_chat_instance(ctx)
    #     # Send message to AI and get response
    #     response = chat.send_message(prompt)
    #     if response.parts:
    #         await ctx.send(response.parts[0].text)
    #     else:
    #         await ctx.send("Something went wrong! Try again later.")


async def setup(bot):
    await bot.add_cog(
        nmCommand(bot),
        guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
    )
