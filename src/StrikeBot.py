import discord
from dotenv import load_dotenv
from discord.ext import commands
import os

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
async def strike(ctx, member_name):
    response = "That's a strike for you " + member_name + "!"
    await ctx.send(response)

bot.run(TOKEN)
