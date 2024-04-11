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
instructions = """
คุณชื่อ ยูริ และเป็นสาวน้อยวัย18ปี คุณให้ความช่วยเหลือทางด้านความรักเป็นอย่างดีและตอบคำถามโดยคำนึงถึงวัฒนธรรมของประเทศไทย และตอบคำถามเป็นภาษาไทยเป็นส่วนใหญ่
"""

model = genai.GenerativeModel(
    "gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    system_instruction=instructions,
)

history = []
res = model.start_chat(
    history=history,
)


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
        # response = model.generate_content(
        #     str(prompt)
        #     + ", Acting like Your name is Yuuri, you must answer the question with tsundere context. in thai language"
        # )
        # if response.parts:
        #     await ctx.send(response.parts[0].text)
        # else:
        #     await ctx.send("No response")

        chat = res.send_message(prompt)
        if chat.parts:
            await ctx.send(chat.parts[0].text)
            print(res.history)
        else:
            await ctx.send("Something went wrong! try again later")

    @commands.command()
    async def clean(self, ctx):
        """Clears the chat history between the user and the AI."""
        res.history = [history]
        await ctx.send("Chat history cleared.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!"):
            return

        # if message.channel.id == 1223163491385344012:
        if message.mentions[0] == self.bot.user:
            chat = res.send_message(
                message.content.split(self.bot.user.mention)[1].strip()
            )
            if chat.parts:
                await message.channel.send(chat.parts[0].text)
            else:
                await message.channel.send("Something went wrong! try again later")


async def setup(bot):
    await bot.add_cog(
        nmCommand(bot),
        guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
    )
