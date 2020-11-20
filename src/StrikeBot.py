import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import random
from eyyo_names import get_memberID_from_name
from eyyo_names import get_name_from_memberID
from StrikeList import StrikeList

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!")

strike_list = StrikeList()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name='strike')
async def strike(ctx, membername, reason="None given"):
    userid = get_memberID_from_name(membername)
    if userid:
        member = bot.get_user(userid)
        strike_list.add_strike(userid, reason)
        response = f"{member.mention} just got a strike because of the following reason: {reason}"
        await ctx.send(response)
    else:
        raise commands.BadArgument


@bot.command(name='why')
async def why(ctx, membername=None):
    if not membername:
        membername = ctx.author.name

    memberid = get_memberID_from_name(membername)
    print(f"command 'why': id returned from {membername} is {memberid}")
    if memberid:
        response = ""
        if not strike_list._data[memberid]:
            response = f"Looks like {membername}'s got no strikes on their list. What a good lad!"
        else:
            reason = strike_list.get_last_strike(memberid)
            response = f"Reason for {membername}'s last strike was: `{reason}`"
        await ctx.send(response)
    else:
        raise commands.BadArgument


@bot.command(name='remove')
async def remove(ctx, membername):
    memberid = get_memberID_from_name(membername)
    print(f"command 'remove': id returned from {membername} is {memberid}")
    if memberid:
        response = ""
        if not strike_list._data[memberid]:
            response = f"Looks like {membername}'s got no strikes on their list. What a good lad!"
        else:
            removed = strike_list.remove_last_strike(memberid)
            response = f"Done! {membername}'s last strike which was `{removed}` has been removed!"
        await ctx.send(response)
    else:
        raise commands.BadArgument


@bot.command(name='showall')
async def showall(ctx):
    response = "```\n"
    slist = strike_list.get_all_strikes()
    for memid in slist:
        num = len(slist[memid])
        name = bot.get_user(memid).name
        response += f"{name} \t: {num}\n"

    response += "```"
    await ctx.send(response)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        some_responses = [
            "Hey, how about you type their name correctly eh?",
            "Can you type correctly? Or did you forget how to write their name?",
            "Can you not make a typo in their name? I can't work with this."
        ]
        response = random.choice(some_responses)
        await ctx.send(response)

# @strike.error
# async def strike_error(ctx, error):
#     if isinstance(error, commands.BadArgument):
#         some_responses = [
#             "Hey, how about you type their name correctly eh?",
#             "Can you type correctly? How about you make my life easier and just @ the guy.",
#             "Can you not make a typo in their name? I can't work with this."
#         ]
#         response = random.choice(some_responses)
#         await ctx.send(response)


@bot.command(name='testing')
async def testing(ctx):
    name = bot.get_user(109452980457082880).name
    await ctx.send(name)

bot.run(TOKEN)
