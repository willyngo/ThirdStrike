import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
from os.path import exists
from gbf_roll_simulator import gbf_rolls


intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!", intents = intents)

# User defined variables
element_list = ['fire', 'water', 'earth', 'wind', 'light', 'dark']
gacha = gbf_rolls()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    

@bot.command(name='strike')
async def strike(ctx, membername):
    logCheck(ctx, "strike")
    member = getMember(membername)
    response = f"{member.mention} is a bitch."
    await ctx.send(response)


@bot.command(name='getgrid')
async def getgrid(ctx, membername='-1', element='-1'):
    logCheck(ctx, "getgrid")

    #If user omits second arg, function takes user's name as second arg  
    if membername in element_list:
        element = membername
        membername = ctx.author.name.lower()

    #Make sure element exists
    checkElement(element)

    #Find member
    member = getMember(membername)
    if member:

        #Grid images are named in this specific format {name}_{element}.png
        playername = member.name
        filename = f"src/grids/{playername}_{element}.png"

        #Check if the image exists
        if not os.path.exists(filename):
            raise commands.BadArgument(f"could not find {playername}'s {element} grid")

        #Send to discord
        await ctx.send(file=discord.File(filename))


@bot.command(name='setgrid')
async def setgrid(ctx, membername='-1', element='-1'):
    logCheck(ctx, "setgrid")

    #If user omits second arg, function takes user's name as second arg
    if membername in element_list:
        element = membername
        membername = ctx.author.name.lower()

    #Does not allow setting up another user's grid
    if membername != '-1' and membername != ctx.author.name:
        raise commands.BadArgument("you can't set someone else's grid")

    #Make sure correct element
    checkElement(element)

    #Must accept attachment
    if ctx.message.attachments:
        #TODO: check if attachment is an image

        #Make sure that naming format of images are {username}_{element}.png
        membername = ctx.author.name.lower()
        filename = f"{membername}_{element}.png"
        print(f"File name to be saved: {filename}")

        #send image to discord
        await ctx.message.attachments[0].save(f"src/grids/{filename}")
        await ctx.send(f"Done! I've set {membername}'s {element} grid.")
    else:
        raise commands.BadArgument("could not find attachments")

@bot.command(name='pull')
async def pull(ctx):
    #pull = gacha.pull()
    pull = gacha.pull()
    response = f'You got {pull}!'
    print(f"{ctx.author.name} pulled {pull}")
    await ctx.send(response)

@bot.command(name='tenpull')
async def tenpull(ctx):
    pulls = gacha.ten_pull()
    response = "Nice! You got: \n"
    print(f'{ctx.author.name} got these: ')
    for pull in pulls:
        response += f'{pull}\n'
        print(f'{pull}')

    await ctx.send(response)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        errorMsg = f"Oops! Something went wrong: {error}."
        print(f"[Exception commands.BadArgument]: {error}.")
        await ctx.send(errorMsg)

# Private functions
def getMember(membername):
    print("-Subcommand: getMember")
    nameToCheck = membername.lower()
    print(f"-member to find: {nameToCheck}")

    for member in bot.get_all_members():
        if nameToCheck == member.display_name.lower() or nameToCheck == member.name.lower():
            print(f"-Member returned: {member.name}")
            return member

    raise commands.BadArgument(f"could not find member: {nameToCheck}")

def checkElement(element):
    if element.lower() not in element_list:
        raise commands.BadArgument(f"no such element: {element}")

def logCheck(ctx, funcName):
    print("**********")
    print(f"Command: {funcName}")
    print(f"Author: {ctx.message.author}")
    print(f"Channel: {ctx.message.channel}")
    print(f"Message: {ctx.message.content}")

def handleError(errorMsg):
    print(errorMsg)

# @bot.command(name='why')
# async def why(ctx, membername=None):
#     if not membername:
#         membername = ctx.author.name

#     memberid = get_memberID_from_name(membername)
#     print(f"command 'why': id returned from {membername} is {memberid}")
#     if memberid:
#         response = ""
#         if not strike_list._data[memberid]:
#             response = f"Looks like {membername}'s got no strikes on their list. What a good lad!"
#         else:
#             reason = strike_list.get_last_strike(memberid)
#             response = f"Reason for {membername}'s last strike was: `{reason}`"
#         await ctx.send(response)
#     else:
#         raise commands.BadArgument


# @bot.command(name='remove')
# async def remove(ctx, membername):
#     memberid = get_memberID_from_name(membername)
#     print(f"command 'remove': id returned from {membername} is {memberid}")
#     if memberid:
#         response = ""
#         if not strike_list._data[memberid]:
#             response = f"Looks like {membername}'s got no strikes on their list. What a good lad!"
#         else:
#             removed = strike_list.remove_last_strike(memberid)
#             response = f"Done! {membername}'s last strike which was `{removed}` has been removed!"
#         await ctx.send(response)
#     else:
#         raise commands.BadArgument


# @bot.command(name='showall')
# async def showall(ctx):
#     response = "```\n"
#     slist = strike_list.get_all_strikes()
#     print("got list")
#     for memid in slist:
#         print("in list")
#         num = len(slist[memid])
#         print(num)
#         print(memid)
#         name = str(bot.get_user(memid))
#         print(name)
#         print("got name")
#         response += f"{name} \t\t: {num}\n"

#     response += "```"
#     await ctx.send(response)




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

bot.run(TOKEN)
