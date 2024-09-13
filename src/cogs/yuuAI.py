import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import requests


load_dotenv()
API_URL = (
    "https://flowise.9lynn.com/api/v1/prediction/55927f33-3576-4755-9eb4-5438ddf6915b"
)
headers = {"Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"}


class yuuAI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!"):
            return

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        if (
            message.channel.id == 1223163491385344012
            or message.mentions[0] == self.bot.user
        ):
            prompt = (
                f"{message.content.replace(self.bot.user.mention, "").strip()}"
                if self.bot.user in message.mentions
                else message.content
            )
            output = query(
                {
                    "question": prompt,
                    "overrideConfig": {
                        "sessionId": f"{message.author.id}",
                    },
                }
            )
            async with message.channel.typing():
                if output is not None:
                    async with message.channel.typing():
                        try:
                            await message.channel.send(output.get("text"))
                        except:
                            await message.channel.send(
                                "Something went wrong! Try again later."
                            )
                else:
                    await message.channel.send("Something went wrong! Try again later.")

    # reset chat session
    # @commands.command()
    # async def reset(self, ctx):


async def setup(bot):
    await bot.add_cog(yuuAI(bot))
