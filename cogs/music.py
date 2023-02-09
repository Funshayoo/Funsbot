import discord
from discord.ext import commands
from discord import app_commands

from youtube_dl import YoutubeDL

from asyncio import run_coroutine_threadsafe, sleep


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color

        # * all the music related stuff
        self.is_playing = False
        self.is_paused = False
        self.is_looped = False

        # ! 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        self.nowplayingsong = ""
        self.nowplayingsource = None

    # ? searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # ? get the first url
            m_url = self.music_queue[0][0]['source']

            # ! remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.song_finished())
        else:
            self.is_playing = False

    # ! infinite loop checking
    async def play_music(self, interaction: discord.Interaction):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # ? try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # ! in case we fail to connect
                if self.vc == None:
                    await self.bot.embed(interaction, "Could not connect to voice channel", ephemeral=True)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # ! remove the first element as you are currently playing it
            self.nowplayingsong = self.music_queue[0][0]['title']
            self.nowplayingsource = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.song_finished())
            self.vc.pause()
            await asyncio.sleep(1)
            self.vc.resume()
        else:
            self.is_playing = False

    def song_finished(self):
        if self.is_looped == True:
            m_url = self.nowplayingsource
            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.song_finished())
        elif len(self.music_queue) > 0:
            self.play_next()
        else:
            self.is_playing = False
            self.is_paused = False
            asyncio.run_coroutine_threadsafe(
                self.vc.disconnect(), self.bot.loop)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded music.py!')

    @app_commands.command(name="play", description="Plays a selected song from youtube")
    @app_commands.guild_only()
    @app_commands.describe(song="What to play")
    async def play(self, interaction: discord.Interaction, song: str):
        query = " ".join(song)

        user_voice = interaction.user.voice
        if user_voice is None:
            # ! you need to be connected so that the bot knows where to go
            await self.bot.embed(interaction, "Connect to the voice channel", ephemeral=True)
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await self.bot.embed(interaction, "Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format", ephemeral=True)
            else:
                await self.bot.embed(interaction, "Song added to the queue")
                self.music_queue.append([song, user_voice.channel])

                if self.is_playing == False:
                    await self.play_music(interaction)

    @app_commands.command(name="pause_on_off", description="Pauses the current song being played")
    @app_commands.guild_only()
    async def resume_or_pause(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await self.bot.embed(interaction, "Pause on")
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await self.bot.embed(interaction, "Pause off")

    @app_commands.command(name="skip", description="Skips the current song being played")
    @app_commands.guild_only()
    async def skip(self, interaction: discord.Interaction):
        if self.vc != None and self.vc:
            self.vc.stop()
            # ! try to play next in the queue if it exists
            await self.play_music(interaction)
            await self.bot.embed(interaction, "Song skipped")

    @app_commands.command(name="queue", description="Displays the current songs in queue")
    @app_commands.guild_only()
    async def queue(self, interaction: discord.Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # ? display a max of 5 songs in the current queue
            if (i > 4):
                break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await self.bot.embed(interaction, retval, title="Queue:")
        else:
            await self.bot.embed(interaction, "No music in queue")

    @app_commands.command(name="queue_clear", description="Stops the music and clears the queue")
    @app_commands.guild_only()
    async def queue_clear(self, interaction: discord.Interaction):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await self.bot.embed(interaction, "Music queue cleared")

    @app_commands.command(name="leave", description="Kick the bot from voice chat")
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await self.bot.embed(interaction, "Bot left the voice chat")

    @app_commands.command(name="nowplaying", description="Prints the current song name")
    @app_commands.guild_only()
    async def nowplaying(self, interaction: discord.Interaction):
        if interaction.user.voice is None or self.is_playing is False:
            await self.bot.embed(interaction, "No song is playing")

        await self.bot.embed(interaction, self.nowplayingsong, title="Now Playing:")

    @app_commands.command(name="loop", description="Loops the song")
    @app_commands.guild_only()
    async def loop(self, interaction: discord.Interaction):
        user_voice = interaction.user.voice
        if user_voice is None:
            # ! you need to be connected so that the bot knows where to go
            await self.bot.embed(interaction, "Connect to the voice channel", ephemeral=True)
        else:
            self.is_looped ^= True
            if self.is_looped == False:
                await self.bot.embed(interaction, "Loop is now off")
            else:
                await self.bot.embed(interaction, "Loop is now on")


async def setup(bot):
    await bot.add_cog(Music(bot))
