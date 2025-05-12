import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import re


load_dotenv()


def query(payload):
    response = requests.post(os.environ.get("FLOWISE_URL"), json=payload)
    return response.json()


class slashCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Commands Ready!")

    @app_commands.command(name="ping", description="A cool ping command!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True
        )

    @app_commands.command(name="ask", description="Ask the AI a question")
    async def ask(self, interaction: discord.Interaction, *, question: str):
        await interaction.response.defer(thinking=True)
        result = query(
            {
                "question": question,
                "overrideConfig": {
                    "sessionId": interaction.user.id,
                },
            }
        )
        print(result)
        await interaction.followup.send(result.get("text"))


async def setup(bot):
    await bot.add_cog(
        slashCommand(bot),
        guilds=[discord.Object(id=785708140959760414)],
    )
