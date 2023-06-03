import discord
from discord.ext import commands
import openai
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

openai.api_key = os.environ.get('OPENAI_API_KEY')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def chatgpt(ctx, *, query):
    try:
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=query,
            max_tokens=50
        )
        reply = response.choices[0].text.strip()

        if len(reply) > 2000:
            chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
            thread_name = f"ChatGPT: {query}"
            thread = await create_thread(ctx, thread_name)
            for chunk in chunks:
                embed = discord.Embed(description=chunk, color=discord.Color.blue())
                await thread.send(embed=embed)
        else:
            embed = discord.Embed(description=reply, color=discord.Color.blue())
            thread_name = f"ChatGPT: {query}"
            thread = await create_thread(ctx, thread_name)
            await thread.send(embed=embed)
    except Exception as e:
        print('Failed to generate response:', e)

async def create_thread(ctx, name):
    guild = ctx.guild
    existing_thread = discord.utils.get(guild.threads, name=name)
    if existing_thread:
        return existing_thread
    else:
        thread = await ctx.channel.create_thread(name=name)
        return thread

bot.run(os.environ.get('DISCORD_TOKEN'))
