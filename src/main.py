import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keepAlive import keepAlive
import asyncio
import platform

load_dotenv()

# intents = discord.Intents.default()
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)
# , help_command=None


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game(name="made by Lynn")
    )


@client.command(name="load")
async def load(ctx, extension):
    """Loads an extension."""
    await client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")
    print(f"Loaded {extension}")


@client.command(name="unload", aliases=["ul"])
async def unload(ctx, extension):
    """Unloads an extension."""
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}")
    print(f"Unloaded {extension}")


@client.command(name="reload", aliases=["rr"])
async def reload(ctx, extension):
    """Reloads an extension."""
    await client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension}")
    print(f"Reloaded {extension}")


@client.event
async def setup_hook():
    """Load default cogs"""
    not_load_cogs = ["song.py", "reactionrole.py"]
    platform_system = (
        os.listdir("./cogs")
        if platform.system() in ["Windows"]
        # if platform.system() in ["Windows", "Linux"]
        else os.listdir("./src/cogs")
    )
    for filename in platform_system:
        if filename.endswith(".py") and filename not in not_load_cogs:
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog: {filename[:-3]}")


async def main():
    try:
        print("Bot is starting...")
        await client.start(os.environ.get("TOKEN"))
    except discord.LoginFailure:
        print("Invalid token provided.")
    except KeyboardInterrupt:
        print("Bot interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if platform.system() == "Unix":
            os.system("kill 1")


asyncio.run(main())
