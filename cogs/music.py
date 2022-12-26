import discord
from discord.ext import commands
from discord import app_commands
from youtube_dl import YoutubeDL

# TODO add some buttons, and now playing
color = 0x2F3136


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # * all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # ! 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

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
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
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
                    embed = discord.Embed(
                        title="", description="Could not connect to voice channel", color=color)
                    await interaction.response.send_message(embed=embed)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # ! remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded music.py!')

    @app_commands.command(name="play", description="Plays a selected song from youtube")
    @app_commands.describe(song="What to play")
    async def play(self, interaction: discord.Interaction, song: str):
        query = " ".join(song)

        voice_channel = interaction.user.voice.channel
        if voice_channel is None:
            # ! you need to be connected so that the bot knows where to go
            embed = discord.Embed(
                title="", description="Connect to the voice channel", color=color)
            await interaction.response.send_message(embed=embed)
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                embed = discord.Embed(
                    title="", description="Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format", color=color)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="", description="Song added to the queue", color=color)
                await interaction.response.send_message(embed=embed)
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(interaction)

    @app_commands.command(name="pause_on_off", description="Pauses the current song being played")
    async def resume_or_pause(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            embed = discord.Embed(
                title="", description="Pause on", color=color)
            await interaction.response.send_message(embed=embed)
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            embed = discord.Embed(
                title="", description="Pause off", color=color)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="skip", description="Skips the current song being played")
    async def skip(self, interaction: discord.Interaction):
        if self.vc != None and self.vc:
            self.vc.stop()
            # ! try to play next in the queue if it exists
            await self.play_music(interaction)
            embed = discord.Embed(
                title="", description="Song skipped", color=color)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue", description="Displays the current songs in queue")
    async def queue(self, interaction: discord.Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # ? display a max of 5 songs in the current queue
            if (i > 4):
                break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            embed = discord.Embed(
                title="Queue:", description=retval, color=color)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="", description="No music in queue", color=color)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue_clear", description="Stops the music and clears the queue")
    async def queue_clear(self, interaction: discord.Interaction):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        embed = discord.Embed(
            title="", description="Music queue cleared", color=color)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Kick the bot from voice chat")
    async def leave(self, interaction: discord.Interaction):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        embed = discord.Embed(
            title="", description="Bot left the voice chat", color=color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))
