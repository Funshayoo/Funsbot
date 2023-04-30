import discord
from discord.ext import commands
from discord import app_commands

from config import Config

import openai


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Loaded ai.py!')

    @app_commands.command(name="ask_gpt", description="Ask GPT-3 a question")
    @app_commands.describe(prompt="Enter your prompt")
    async def ask_gpt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        openai.api_key = Config.OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=64,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        await self.bot.embed(interaction, title="ChatGPT response: ", description=response.choices[0].text, followup=True)

    # @app_commands.command(name="picture", description="generate a picture from prompt")
    # @app_commands.describe(prompt="Enter your prompt")
    # async def picture(self, interaction: discord.Interaction, prompt: str):
    #     await interaction.response.defer()


async def setup(bot):
    await bot.add_cog(Ai(bot))
