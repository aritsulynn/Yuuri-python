import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

channel_id = int(os.getenv('channel_id'))
message_id = int(os.getenv('message_id'))
emoji_to_react_with = os.getenv('emoji_to_react_with')
role_to_give = os.getenv('role_to_give')

class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): 
        await self.bot.wait_until_ready()
        message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        await message.add_reaction(emoji_to_react_with)
        print("Reaction Roles Ready!")
        # check if bot offline and someone reacts, then add role


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        if payload.guild_id is None:
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=role_to_give)
        member = guild.get_member(payload.user_id)
        if payload.channel_id == channel_id and payload.message_id == message_id and str(payload.emoji) == emoji_to_react_with:
            await member.add_roles(role)
            print("Reaction Role Added!")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        if payload.guild_id is None:
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=role_to_give)
        member = guild.get_member(payload.user_id)
        if payload.channel_id == channel_id and payload.message_id == message_id and str(payload.emoji) == emoji_to_react_with:
            await member.remove_roles(role)
            print("Reaction Role Removed!")

async def setup(bot):
    await bot.add_cog(reactionrole(bot), guilds=[discord.Object(id=int(i)) for i in os.getenv('guilds').split(',')])