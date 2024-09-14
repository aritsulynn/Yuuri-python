import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import re
from upstash_redis import Redis


load_dotenv()
API_URL = "http://flowise:3001/api/v1/prediction/55927f33-3576-4755-9eb4-5438ddf6915b"
# API_URL = (
#     "https://flowise.9lynn.com/api/v1/prediction/55927f33-3576-4755-9eb4-5438ddf6915b"
# )
headers = {"Authorization": f"Bearer {os.getenv("BEARER_TOKEN")}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class slashCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis = Redis(url=os.getenv("UPSTASH_REDIS_REST_URL"), token=os.getenv("UPSTASH_REDIS_REST_TOKEN"))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Commands Ready!")

    @app_commands.command(name="ping", description="A cool ping command!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True
        )

    @app_commands.command(name="ask", description="Ask a question!")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Ask AI command!"""
        await interaction.response.defer(ephemeral=True)
        output = query(
            {
                "question": question,
                "overrideConfig": {
                    "sessionId": f"{interaction.user.id}",
                },
            }
        )
        print(interaction.user.name + " asked: " + question)
        await interaction.followup.send(output["text"], ephemeral=True)

    @app_commands.command(name="reset", description="Reset the chat session!")
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        status = self.redis.delete(str(interaction.user.id))
        if status:
            await interaction.followup.send("Chat session reset successfully!")
        else:
            await interaction.followup.send("Chat session not found!")

async def setup(bot):
    await bot.add_cog(
        slashCommand(bot),
        guilds=[discord.Object(id=int(i)) for i in os.getenv("guilds").split(",")],
    )
