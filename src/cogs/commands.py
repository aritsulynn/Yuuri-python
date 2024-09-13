import os
import random
import discord
from discord.ext import commands
from datetime import datetime

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi


class nmCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.client = MongoClient("your-mongodb-connection-string")
        # self.db = self.client["mydatabase"]
        # self.collection = self.db["mycollection"]
        # self.client = MongoClient(os.getenv("mongodbURI"), server_api=ServerApi("1"))
        # self.db = self.client["yuu-test"]
        # self.collection = self.db["yuu-collection"]
        # try:
        #     self.client.admin.command("ping")
        #     print("ping mongo")
        # except Exception as e:
        #     print("failed to ping")

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

    @commands.command(name="random")
    async def random(self, ctx):
        print("random")
        list = ["A", "B", "C"]
        await ctx.reply(f"I choose {random.choice(list)}")

    # @commands.command(name="test")
    # async def test(self, ctx):
    #     user_data = {"user_id": ctx.author.id, "user_name": ctx.author.name}
    #     self.collection.insert_one(user_data)
    #     await ctx.send(f"User {user_data} added to the database.")

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
