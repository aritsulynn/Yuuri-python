import asyncio
import discord 
from discord.ext import commands
from discord import app_commands
import logging
# from typing import cast
from typing import cast
import wavelink

class song(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        discord.utils.setup_logging(level=logging.INFO)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Wavelink Commands Ready!")
        await self.bot.wait_until_ready()
        nodes = [wavelink.Node(uri="http://127.0.0.1:2333", password="youshallnotpass")]
        await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        print(f"Node {payload.node!r} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)

    "check if the song end and there is a next song in the queue"
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        # Check for next song in the queue
        next_track = await player.queue.get_wait()

        if next_track is not None:
            # Play the next song
            await player.play(next_track)
        else:
            await player.home.send("Queue is empty, disconnecting...")
            # timeout 
            await asyncio.sleep(30)
            await player.disconnect()

    @app_commands.command(name="play", description="play a song")
    async def play(self, interaction: discord.Interaction, *, query: str):
        """Play a song with a given query or URL."""
        print("playing: ", query)
        if not interaction.guild:
            return
        
        player: wavelink.Player 
        player = cast(wavelink.Player, interaction.guild.voice_client)
        
        print("player: ", player)

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await interaction.followup.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await interaction.followup.send("I was unable to join this voice channel. Please try again.")
                return
            
        await interaction.response.send_message("Thinking...")
        # await interaction.followup.send(f"{query}")

        # Turn on AutoPlay to enabled mode.
        # enabled = AutoPlay will play songs for us and fetch recommendations...
        # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
        # disabled = AutoPlay will do nothing...
        # player.autoplay = wavelink.AutoPlayMode.disabled

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = interaction.channel
        elif player.home != interaction.channel:
            await interaction.response.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        # This will handle fetching Tracks and Playlists...
        # Seed the doc strings for more information on this method...
        # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
        # Defaults to YouTube for non URL based queries...
        tracks: wavelink.Search = await wavelink.Playable.search(query)

        # print("tracks: ", tracks)
        if not tracks:
            await interaction.followup.send(f"{interaction.user.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)
            await interaction.followup.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await interaction.followup.send(f"Added **`{track}`** to the queue.")

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

        # # Optionally delete the invokers message...
        # try:
        #     # await interaction.response.message.delete()
        #     await interaction.followup.delete()
        # except discord.HTTPException:
        #     pass

    @app_commands.command(name="join", description="join a voice channel")
    async def join(self, interaction: discord.Interaction):
        """Join a voice channel."""
        member = interaction.user
        voice_state = member.voice
        if not voice_state or not voice_state.channel:
            await interaction.response.send_message("You are not currently in a voice channel.")
            return
        channel = voice_state.channel
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}!")

    @app_commands.command(name="leave", description="leave a voice channel")
    async def disconnect(self, interaction: discord.Interaction) -> None:
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        await player.disconnect()
        await interaction.response.send_message("Disconnected!")

    @app_commands.command(name="pause", description="pause the player")
    async def pause(self, interaction: discord.Interaction) -> None:
        """Pause or Resume the Player depending on its current state."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        # await ctx.message.add_reaction("\u2705")
        await interaction.response.send_message("Paused!")

    @app_commands.command(name="resume", description="resume the player")
    async def resume(self, interaction: discord.Interaction) -> None:
        """Resume the Player."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await interaction.response.send_message("Resumed!")

    @app_commands.command(name="skip", description="skip the current song")
    async def skip(self, interaction: discord.Interaction) -> None:
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await interaction.response.send_message("Skipped!")


    @app_commands.command(name="queue", description="show the queue")
    async def queue(self, interaction: discord.Interaction) -> None:
        """Show the current queue."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        embed: discord.Embed = discord.Embed(title="Queue")
        embed.description = "\n".join(f"**`{i + 1}.`** {track}" for i, track in enumerate(player.queue[:5]))
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="nowplaying", description="show the current song")
    async def nowplaying(self, interaction: discord.Interaction) -> None:
        """Show the currently playing song."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player or not player.current:
            return

        track: wavelink.Playable = player.current
        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**`{track.title}`** by `{track.author}`"
        if track.artwork:
            embed.set_image(url=track.artwork)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="volume", description="change the volume")
    async def volume(self, interaction: discord.Interaction, *, volume: int) -> None:
        """Change the Player's volume."""
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            return

        await player.set_volume(volume)
        await interaction.response.send_message(f"Volume set to {volume}!")

    # @app_commands.command(name="shuffle", description="shuffle the queue")
    # async def shuffle(self, interaction: discord.Interaction) -> None:
    #     """Shuffle the current queue."""
    #     player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
    #     if not player:
    #         return

    #     player.queue.shuffle()
    #     await interaction.response.send_message("Shuffled!")

async def setup(bot):
    await bot.add_cog(song(bot), guilds=[discord.Object(id=785708140959760414)])