import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import requests


key = "1f95e16c-d1ff-461f-97c2-70b3cc6e6c0b"
main_key = "55927f33-3576-4755-9eb4-5438ddf6915b"
API_URL = f"http://host.docker.internal:5000/api/v1/prediction/{main_key}"

load_dotenv()


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
            response = requests.post(API_URL, json=payload)
            return response.json()

        if (
            message.channel.id == 1223163491385344012
            or message.mentions[0] == self.bot.user
        ):
            print("Message received 2")
            prompt = (
                f"{message.content.split(self.bot.user.mention)[1].strip()}"
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
                            await message.channel.send(output["text"])
                        except:
                            await message.channel.send(
                                "Something went wrong! Try again later."
                            )
                else:
                    await message.channel.send("Something went wrong! Try again later.")


async def setup(bot):
    await bot.add_cog(yuuAI(bot))
