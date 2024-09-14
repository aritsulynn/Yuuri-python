import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import requests
import re
from upstash_redis import Redis

load_dotenv()
API_URL = "http://flowise:3001/api/v1/prediction/55927f33-3576-4755-9eb4-5438ddf6915b"
# API_URL = "https://flowise.9lynn.com/api/v1/prediction/55927f33-3576-4755-9eb4-5438ddf6915b"
headers = {"Authorization": f"Bearer {os.getenv("BEARER_TOKEN")}"}

class yuuAI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.redis = Redis(url=os.getenv("UPSTASH_REDIS_REST_URL"), token=os.getenv("UPSTASH_REDIS_REST_TOKEN"))
        print(self.redis.ping())

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
            message.channel.id in [1223163491385344012]
            or message.mentions[0] == self.bot.user
        ):
            
            prompt = re.sub(r'<@\d+>', '', message.content)
            output = query(
                {
                    "question": prompt,
                    "overrideConfig": {
                        "sessionId": f"{message.author.id}",
                    },
                }
            )
            # print(output['text'])
            async with message.channel.typing():
                if output is not None:
                    async with message.channel.typing():
                        try:
                            await message.channel.send(output['text'])
                        except:
                            await message.channel.send(
                                "Something went wrong! Try again later."
                            )
                else:
                    await message.channel.send("Something went wrong! Try again later.")

    # reset chat session
    @commands.command()
    async def reset(self, ctx):
        status = self.redis.delete(str(ctx.author.id))
        if status:
            await ctx.send("Chat session reset successfully!")
        else:
            await ctx.send("Chat session not found!")


async def setup(bot):
    await bot.add_cog(yuuAI(bot))
