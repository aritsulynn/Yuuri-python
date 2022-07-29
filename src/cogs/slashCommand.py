import time
from turtle import update
from discord import SlashOption
import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
import requests
from .customFunction import myFunction as mf
from .customFunction import updateanime as updateanime

import datetime
import asyncio

class slashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.run_task.start()

    @nextcord.slash_command(name="rank", description="Get valorant current rank")
    async def rank(self, interaction: Interaction, *, name : str = SlashOption(name='name', description='Insert your game name.', required=True), tag : str = SlashOption(name='tag', description='Insert your tag.', required=True)):
        await interaction.response.defer(with_message=True,ephemeral=False)
        # https://api.kyroskoh.xyz/valorant/v1/mmr/ap/ID/Tag
        await interaction.followup.send(f'{name}#{tag} is ' + requests.get(f'https://api.kyroskoh.xyz/valorant/v1/mmr/ap/{name}/{tag}').text)
    
    @tasks.loop(seconds=5.0)
    async def run_task(self):
        # check if the bot is online
        lists = []
        count = 0
        if self.bot.is_ready():
            channel = self.bot.get_channel(1002559144999538748)
            # await channel.send(updateanime.get_update())
            if updateanime.check_update_or_not() == True:
                await channel.send("https://i.imgur.com/Q4xuDua.png")
                for i in updateanime.send_update():
                    count += 1
                    lists.append(f"{count}. `{i}`" )
                await channel.send(''.join(lists))
                updateanime.update_last_update()

def setup(bot):
    bot.add_cog(slashCommands(bot))
