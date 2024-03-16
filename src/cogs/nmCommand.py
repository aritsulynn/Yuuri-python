import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel("gemini-pro", safety_settings=safety_settings)


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

    @commands.command()
    async def ask(self, ctx, *, prompt):
        """Ask AI command!"""
        response = model.generate_content(str(prompt))
        if response.parts:
            await ctx.send(response.text)
        else:
            await ctx.send("Something went wrong!")


async def setup(bot):
    await bot.add_cog(
        nmCommand(bot),
        guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
    )
