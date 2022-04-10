import os
import time
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from .customFunction import myFunction as mf


class slashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
        
def setup(bot):
    bot.add_cog(slashCommands(bot))
