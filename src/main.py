from prettytable import PrettyTable
from nextcord import Intents
from nextcord.ext import commands
import nextcord
import os
from dotenv import load_dotenv
from keepAlive import keepAlive
load_dotenv()

intents = nextcord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="+", intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(name="@aritsu#1667"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

table =  PrettyTable(["Name", "Status"])
for fn in os.listdir("./src/cogs"):
# for fn in os.listdir("./cogs"): # ubuntu
    if fn.endswith(".py"):
        client.load_extension(f"cogs.{fn[:-3]}")
        # print("Load :" + fn)
        table.add_row([f"cogs.{fn[:-3]}", "Loaded"])
print(table)

@client.command(name="load")
async def load(ctx, extension):
    """Loads an extension."""
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")
    print(f"Loaded {extension}")

@client.command(name="unload", aliases=["ul"])
async def unload(ctx, extension):
    """Unloads an extension."""
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}")
    print(f"Unloaded {extension}")

@client.command(name = "reload", aliases=["rr"])
async def reload(ctx, extension):
    """Reloads an extension."""
    client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension}")
    print(f"Reloaded {extension}")


# keepAlive()
# try:
client.run(os.environ.get('TOKEN'))
# except:
#   os.system("kill 1")