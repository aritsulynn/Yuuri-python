import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

safety_settings = {
    "HATE": "BLOCK_NONE",
    "HARASSMENT": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}


model = genai.GenerativeModel(
    "gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    system_instruction=os.getenv("AI_INSTRUCTIONS"),
    # generation_config={
    #     "temperature": 0.6,
    #     "max_output_tokens": 1024,
    #     "candidate_count": 1,
    #     "stop_sequences": ["\n"],
    # },
)

history = []
chat = model.start_chat(history=history)


class gemAI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!"):
            return

        # if channel is 1223163491385344012 it will be responded to by the AI
        # print(message.channel.id)

        if (
            message.channel.id == 1223163491385344012
            or message.mentions[0] == self.bot.user
        ):
            prompt = (
                f"{message.author.name} : {message.content.split(self.bot.user.mention)[1].strip()}"
                if self.bot.user in message.mentions
                else message.content
            )
            async with message.channel.typing():
                res = chat.send_message(prompt)
                if res.parts:
                    text = res.parts[0].text
                    if len(text) > 2000:
                        for i in range(0, len(text), 2000):
                            await message.channel.send(text[i : i + 2000])
                    else:
                        await message.channel.send(text)
                else:
                    await message.channel.send("Something went wrong! Try again later.")

    # clear chat history
    @commands.command()
    async def clear(self, ctx):
        global chat
        chat = model.start_chat(history=[])
        await ctx.send("Chat history cleared!")

    # get chat history
    @commands.command()
    async def history(self, ctx):
        await ctx.send(history)


async def setup(bot):
    await bot.add_cog(gemAI(bot))
