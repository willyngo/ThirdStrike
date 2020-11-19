import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import random
from Strike import Strike

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name='strike')
async def strike(ctx, member: discord.Member = None, reason="None given"):
    response = f"{member.name} just got a strike because of the following reason: {reason}"
    await ctx.send(response)


@strike.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        some_responses = [
            "Hey, how about you type the guy's name correctly eh?",
            "Can you type correctly? How about you make my life easier and just @ the guy.",
            "Can you not make a typo in the guy's name? I can't work with this."
        ]
        response = random.choice(some_responses)
        await ctx.send(response)


@bot.command(name='testing')
async def testing(ctx):
    response = "HELLO"
    await ctx.send(response)

bot.run(TOKEN)
