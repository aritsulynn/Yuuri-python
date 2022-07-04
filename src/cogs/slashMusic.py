from discord import SlashOption
import nextcord
import wavelink
from nextcord.abc import GuildChannel
from nextcord.ext import commands
from wavelink.ext import spotify
import os
import yarl
from nextcord import Interaction
import asyncio
from cogs.customFunction import musicHelper as mHelper

spotifyClient = os.getenv("spotifyClient")
spotifySecret = os.getenv("spotifySecret")

class slashMusic(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()
        # await wavelink.NodePool.create_node(bot=self.bot,
        #                                     host='lava.link',
        #                                     port=80,
        #                                     password='YOUR_LAVALINK_PASSWORD',
        #                                     identifier='lavalink',
        #                                     spotify_client=spotify.SpotifyClient(client_id=spotifyClient, client_secret=spotifySecret))

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='kartadharta.xyz',
                                            port=3000,
                                            password="kdlavalink",
                                            identifier='Wavelink',
                                            spotify_client=spotify.SpotifyClient(client_id=spotifyClient, client_secret=spotifySecret))

    # on start the bot will connect to the nodes
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    # if song end 
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason: str):
        """Event fired when a track ends."""
        interaction = player.interaction

        if not player.queue.is_empty:
            next_song = player.queue.get()
            await player.play(next_song)
            await interaction.edit_original_message(embed=mHelper.controller(next_song.title, mHelper.convert_time(next_song.duration), next_song.uri, next_song.thumb))
        
        def check(p: wavelink.Player):
            return p.guild == player.guild
        try:
            await self.bot.wait_for("wavelink_track_start", check=check, timeout=60)  # waits for 'on_wavelink_track_start'
        except asyncio.TimeoutError:  # bot didn't play any tracks for 1 minutes
            await interaction.delete_original_message(delay=0)
            await player.disconnect()

    # play 
    @nextcord.slash_command(name= "play" , description="Play a song")
    async def play(self, interaction: Interaction, *, url: str = SlashOption(name="url", description="Insert your song url or your song name to play!", required=True)):
        """Play a song from YouTube Track or Playlist."""
        await interaction.response.defer(with_message=True)

        try:
            # if bot is not in a voice channel
            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(reconnect=True, cls=wavelink.Player)
            # if in a voice channel
            else:
                vc: wavelink.Player = interaction.guild.voice_client
        except:
            await interaction.followup.send(embed=mHelper.error_embed("I'm not in a voice channel!"))
            return
            
        decoded = spotify.decode_url(url)
        # check it's a spotify track
        if decoded and decoded['type'] is spotify.SpotifySearchType.track:
            track = await spotify.SpotifyTrack.search(query=url, return_first=True)
            await vc.queue.put_wait(track)
            
        # check it's a spotify playlist
        elif decoded and decoded['type'] is spotify.SpotifySearchType.playlist:
            async for track in spotify.SpotifyTrack.iterator(query=url, type=spotify.SpotifySearchType.playlist):
                if not vc.is_playing():
                    await vc.play(track)
                    await interaction.followup.send(embed=mHelper.controller(track.title, mHelper.convert_time(track.duration), track.uri, track.thumb))
                else:
                    await vc.queue.put_wait(track)

        # check spotify album
        elif decoded and decoded['type'] is spotify.SpotifySearchType.album:
            async for track in spotify.SpotifyTrack.iterator(query=url, type=spotify.SpotifySearchType.album):
                if not vc.is_playing():
                    await vc.play(track)
                    await interaction.followup.send(embed=mHelper.controller(track.title, mHelper.convert_time(track.duration), track.uri, track.thumb))
                else:
                    await vc.queue.put_wait(track)
                # print(f'Track: <{track.title}> added to queue.')
        # check youtube uri
        else:
            # check playlist or not
            check = yarl.URL(url)
            if check.query.get("list"):
                playlist =  await wavelink.YouTubePlaylist.search(url)
                for song in playlist.tracks:
                    vc.queue.put(song)
                    print(song.title)
                if vc.is_playing():
                    await interaction.followup.send(embed = mHelper.embed_msg(f"Added {len(playlist.tracks)} songs to queue."), delete_after=10)
            else:
                track = await wavelink.YouTubeTrack.search(query=url, return_first=True)
                vc.queue.put(track)
                # print(track.title)
                if vc.is_playing():
                    await interaction.followup.send(embed=mHelper.embed_msg(f"Add {track.title} to the queue."), delete_after=10)
        
        if not vc.is_playing():
            track = await vc.play(vc.queue.get())
            await interaction.followup.send(embed=mHelper.controller(track.title, mHelper.convert_time(track.duration), track.uri, track.thumb))
            vc.interaction = interaction

        # vc.user = interaction.user

    # skip
    @nextcord.slash_command(name= "skip", description="Skip a song")
    async def skip(self, interaction: Interaction):
        """Skip the current song."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed=mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed=mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        if vc.queue.is_empty():
            await interaction.response.send_message(embed=mHelper.embed_msg("Queue is empty."), delete_after=10)
            return
        await vc.stop()
        await interaction.response.send_message(embed=mHelper.embed_msg("Skipped the song."), delete_after=10)

    # queue
    @nextcord.slash_command(name= "queue" , description="Show the queue")
    async def queue(self, interaction: Interaction):
        """Show the current queue."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed=mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if vc.queue.is_empty:
            await interaction.response.send_message(embed=mHelper.embed_msg("The queue is empty."), delete_after=10)
            return
        songs = [f"`{i + 1}.` {song.title}" for i, song in enumerate(vc.queue._queue)]
        await interaction.response.send_message(embed=mHelper.queue_list(songs))

    # pause
    @nextcord.slash_command(name= "pause" , description="Pause the current song")
    async def pause(self, interaction: Interaction):
        """Pause the current song."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        vc.pause()
        await interaction.response.send_message(embed = mHelper.embed_msg("Paused the song."), delete_after=10)

    # resume
    @nextcord.slash_command(name= "resume", description="Resume the current song")
    async def resume(self, interaction: Interaction):
        """Resume the current song."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        vc.resume()
        await interaction.response.send_message(embed = mHelper.embed_msg("Resumed the song."), delete_after=10)

    # volume
    @nextcord.slash_command(name= "volume" , description="Change the volume")
    async def volume(self, interaction: Interaction, *, volume: int = SlashOption(name="volume", description="Insert your volume here!", required=True)):
        """Set the volume of the player."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        if volume >= 0 or volume <= 100:
            await interaction.response.send_message(embed = mHelper.embed_msg(f"Volume set to {volume}%."), delete_after=10)
            return await vc.set_volume(volume)
        else:
            await interaction.response.send_message(embed = mHelper.embed_msg("Volume must be between 0 and 100."), delete_after=10)

    # connect
    @nextcord.slash_command(name= "connect", description="Connect to a voice channel")
    async def connect(self, interaction: Interaction):
        """Connect to a voice channel."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.user.voice.channel.connect(cls=wavelink.Player)
            await interaction.response.send_message(embed = mHelper.embed_msg("Connected to the voice channel."), delete_after=10)
            return
        if vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("I am already connected to a voice channel."), delete_after=10)
            return

    # disconnect
    @nextcord.slash_command(name= "disconnect" , description="Disconnect from a voice channel")
    async def disconnect(self, interaction: Interaction):
        """Disconnect the bot from the voice channel."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        await vc.disconnect()
        await interaction.response.send_message(embed = mHelper.embed_msg("Disconnected from the voice channel."), delete_after=10)

    # clearqueue
    @nextcord.slash_command(name= "clearqueue", description="Clear the queue")
    async def clearqueue(self, interaction: Interaction):
        """Clear the queue."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if vc.queue.is_empty:
            await interaction.response.send_message(embed = mHelper.embed_msg("The queue is empty."), delete_after=10)
            return
        vc.queue.clear()
        await interaction.response.send_message(embed = mHelper.embed_msg("Cleared the queue."), delete_after=10)
    

    # now playing 
    @nextcord.slash_command(name= "nowplaying", description="Show the current song")
    async def nowplaying(self, interaction: Interaction):
        """Show the current song."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        await interaction.response.send_message(embed=mHelper.controller(vc.track.title, mHelper.convert_time(vc.track.duration), vc.track.uri, vc.track.thumb))
    
    #stop
    @nextcord.slash_command(name= "stop", description="Stop the current song")
    async def stop(self, interaction: Interaction):
        """Stop the current song."""
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message(embed = mHelper.embed_msg("I am not in a voice channel."), delete_after=10)
            return
        if not vc.is_playing():
            await interaction.response.send_message(embed = mHelper.embed_msg("Nothing is playing."), delete_after=10)
            return
        vc.queue.clear()
        await vc.stop()
        await interaction.response.send_message(embed = mHelper.embed_msg("Stopped the song."), delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(slashMusic(bot))
