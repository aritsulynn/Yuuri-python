import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keepAlive import keepAlive
import asyncio

load_dotenv()

# intents = discord.Intents.default()
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)
# , help_command=None


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(status=discord.Status.idle,
                               activity=discord.Game(name="_douzo"))


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
  # for filename in os.listdir('./cogs'):
  for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
      await client.load_extension(f'cogs.{filename[:-3]}')
      print(f"Loaded Cog: {filename[:-3]}")


async def main():
  keepAlive()
  try:
    await client.start(os.environ.get('TOKEN'))
  except:
    os.system("kill 1")


asyncio.run(main())
