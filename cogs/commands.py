import os
import random
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import asyncio

import requests

load_dotenv()


def query(payload):
    response = requests.post(os.environ.get("FLOWISE_URL"), json=payload)
    return response.json()


class nmCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        print("ping")
        print(ctx.author)
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
        print("test")

    @commands.command()
    async def ask(self, ctx, *, question):
        # await ctx.send("Asking the AI...")
        result = query(
            {
                "question": question,
                "overrideConfig": {
                    "sessionId": ctx.author.id,
                },
            }
        )
        print(result)
        await ctx.reply(result.get("text"))


async def setup(bot):
    await bot.add_cog(
        nmCommand(bot),
        # guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
        guilds=[discord.Object(id=785708140959760414)],
    )
