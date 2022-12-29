import discord
from discord.ext import commands
from discord import app_commands
import random


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.embed_color
        self.is_playing = False
        self.answer = ""
        self.user_guess = ""

        # * all word dictionaries
        self.popular = open(
            "./wordle_src/wordle_words.txt").read().splitlines()
        self.all_words = open(
            "./wordle_src/dictionary.txt").read().splitlines()

    async def get_random_word(self) -> str:
        wordle_word = self.popular
        return random.choice(wordle_word)

    async def generate_blanks(self) -> str:
        return ((":white_medium_square:" * 5) + ("\n")) * 6

    async def is_word_valid(self, word: str) -> bool:
        valid = False
        if word in self.all_words:
            valid = False
            return valid
        else:
            valid = True
            return valid

    async def generate_colored_word(self, guess: str, answer: str) -> str:
        # colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
        # guess_letters: List[Optional[str]] = list(guess)
        # answer_letters: List[Optional[str]] = list(answer)
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                # colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
                answer[i] = None
                guess[i] = None

        for i in range(len(guess)):
            if guess[i] is not None and guess[i] in answer:
                # colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
                answer[answer.index(guess[i])] = None

        # return "".join(colored_word)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded wordle.py!')

    # TODO wordle command
    @app_commands.command(name="wordle_play", description="Play a game of wordle")
    async def play_wordle(self, interaction: discord.Interaction):
        if self.is_playing:
            embed = discord.Embed(
                title="", description="Game is already started", color=self.color)
            await interaction.response.send_message(
                embed=embed, ephemeral=True)
        else:
            self.is_playing = True
            self.is_playing = True
            self.answer = await self.get_random_word()
            blanks = await self.generate_blanks()
            embed = discord.Embed(title="Guees the word using: **/wordle_guess**",
                                  description=f"{blanks}", color=self.color)
            await interaction.response.send_message(embed=embed)

    @ app_commands.command(name="wordle_guess", description="Guess a word")
    @ app_commands.describe(guess="Your guess")
    async def wordle_guess(self, interaction: discord.Interaction, guess: str):
        if self.is_playing == False:
            embed = discord.Embed(
                title="", description="You need to start the game first by using **/wordle_play**", color=self.color)
            await interaction.response.send_message(embed=embed)
        else:
            word_valid = await self.is_word_valid(guess.lower())
            if word_valid == False:
                self.user_guess = guess.lower()
                await interaction.response.defer(thinking=True)
                await interaction.channel.send(f"{guess}")
                await interaction.channel.purge(limit=2)
                color_word = await self.generate_colored_word(self.user_guess, self.answer)
            else:
                embed = discord.Embed(
                    title="", description="Your word is not in dictionary", color=self.color)
                await interaction.response.send_message(embed=embed)

    @ app_commands.command(name="wordle_stats", description="view wordle stats")
    async def wordle_stats(self, interaction: discord.Interaction):
        pass


async def setup(bot):
    await bot.add_cog(Wordle(bot))
