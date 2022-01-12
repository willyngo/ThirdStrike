import discord
import os
import json
from discord.errors import NotFound
from discord.ext.commands.errors import UserNotFound
from dotenv import load_dotenv
from discord.ext import commands
from os.path import exists
from gbf_roll_simulator import gbf_rolls
from StrikeDB import StrikeDB

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!", intents = intents)

# User defined variables
element_list = ['fire', 'water', 'earth', 'wind', 'light', 'dark']
gacha = gbf_rolls()
user_db = StrikeDB()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    

@bot.command(name='strike')
async def strike(ctx, membername, *, reason="no reason apparantly"):
    """
    Give someone a strike
    """
    logCheck(ctx, "strike")
    member = getMember(membername)
    user_db.addStrike(member, reason)
    response = f"{member.mention} is a bitch for the following reason: {reason}."
    await ctx.send(response)

@bot.command(name='why')
async def strike(ctx, membername=None):
    """
    Get list of strikes
    """
    logCheck("why")
    if membername is None:
        membername = ctx.author.name
    
    member = getMember(membername)
    strikelist = user_db.getStrikes(member)

    response = f"Here are {membername}'s list of strikes:\n"
    for i in strikelist:
        response += f"{i}\n"
    
    await ctx.send(response)

@bot.command(name='getgrid')
async def getgrid(ctx, membername='-1', element='-1'):
    """
    Get someone's grid. Specify username and element.
    """
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
    """
    Sets attached image to grid element.
    """
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
    """
    Pull a single time using 300 crystals
    """
    logCheck(ctx, "Pull")
    pull = []
    #check crystals before pulling
    amount = user_db.getCrystal(ctx.author)
    if amount > 300:
        user_db.removeCrystal(ctx.author, 300)
        pull.append(gacha.pull())
        embed = makePullsEmbed(ctx, pull)
    else:
        embed = discord.Embed(title="Sorry!", 
        description=f"Looks like you're running a little low there. You need at least 300 crystals for a single pull but you've only got {amount}.")

    await ctx.send(embed=embed)

@bot.command(name='tenpull')
async def tenpull(ctx):
    """
    Pull 10 times using 3000 crystals
    """
    logCheck(ctx, "TenPull")

    amount = user_db.getCrystal(ctx.author)
    if amount > 3000:
        user_db.removeCrystal(ctx.author, 3000)
        pulls = gacha.ten_pull()
        embed = makePullsEmbed(ctx, pulls)
        # response = "Nice! You got: \n"
        # print(f'{ctx.author.name} got these: ')
        # for pull in pulls:
        #     response += f'{pull}\n'
        #     print(f'{pull}')
        # response += f"You have {user_db.getCrystal(ctx.author)} crystals remaining."
    else:
        embed = discord.Embed(title="Sorry!", 
        description=f"Looks like you're running a little low there. You need at least 3000 crystals for a 10-pull but you've only got {amount}.")

    await ctx.send(embed=embed)

@bot.command(name='daily')
async def daily(ctx):
    """
    Get daily bonus!
    """
    logCheck(ctx, "daily")
    #user_id = ctx.author.id
    author = ctx.author
    response = ""

    if not user_db.getDaily(author):
        response = "You've already redeemed your login bonus. Greedy Bitch."
    else:
        response = f"Thanks for logging in! You've earned 3000 crystals. You now have {user_db.getCrystal(author)} crystals."
    
    await ctx.send(response)

@bot.command(name='resetdaily')
async def resetDaily(ctx):
    """
    reset daily bonus [test]
    """
    logCheck(ctx, "resetDaily")
    user_db.resetDaily()
    response = "Daily bonuses have been reset!"
    print(response)
    await ctx.send(response)

@bot.command(name='addcrystal')
@commands.has_role('Mods')
async def addCrystal(ctx, amount):
    """
    Adds crystal to user [test]
    """
    logCheck(ctx, "addCrystal")
    author = ctx.author

    user_db.addCrystal(author, amount)
    response = f"Nice! We've added your crystals, you now have {user_db.getCrystal(author)} crystals."
    print(response)
    await ctx.send(response)

@bot.command(name='crystal')
async def getCrystal(ctx):
    """
    Show current amount of crystals
    """
    logCheck(ctx, "getCrystal")

    id = ctx.author
    amount = user_db.getCrystal(ctx.author)

    response = f"Hi {ctx.author.display_name}! You currently have {amount} crystals."
    await ctx.send(response)

@bot.command(name='status')
async def status(ctx):
    """
    Check user status [test] 
    """
    logCheck(ctx, "status")
    response = user_db.getUser(ctx.author)

    if not response:
        response = "Sorry, it seems like we couldn't find you and it looks like willyngo didn't make me auto add you if you weren't in the db already. What a lazy ass."

    await ctx.send(response)

# Error handling
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.BadArgument):
        errorMsg = f"Oops! Something went wrong, {error}. Please refer to the !help {ctx.command}"
        print(f"[Exception commands.BadArgument]: {error}.")
    if isinstance(error, commands.UserNotFound):
        willy = getMember("willyngo")
        errorMsg = f"Oops! Looks like we couldn't find the user. {willy.mention} should've made me add you to the db automatically but he's being a lazy bum right now."
        print(f"[Exception commands.UserNotFound]: {error}")
    else:
        errorMsg = f"Oops! Something went wrong: {error}"
        print(errorMsg)
    
    await ctx.send(errorMsg)

# Private functions
def makePullsEmbed(ctx, pulls):
    pull_embed = discord.Embed(title=f"{ctx.author.display_name}'s pulls!",
        description="Here's what you got:",
        color=0xFF5733)
    i = 1
    for item in pulls:

        #Add an empty field to correct embed formatting
        if i % 2 == 0:
            pull_embed.add_field(name='\u200b', value='\u200b')

        rare = item['rarity']
        style = ""
        if rare == 'sr':
            style = "yaml"
        elif rare == "ssr":
            style = "fix"

        fieldvalue = f"```{style}\n{item['name']}\n```"
        fieldname = f"{item['type']} | {item['rarity'].upper()}"
        
        pull_embed.add_field(name=fieldname, value=fieldvalue)
        i+=1
        
    pull_embed.add_field(name='\u200b', value='\u200b')
    pull_embed.set_thumbnail(url=ctx.author.avatar_url)
    pull_embed.set_footer(text=f"You have {user_db.getCrystal(ctx.author)} crystals remaining.")

    return pull_embed

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

def logCheck(ctx, funcName, msg="None"):
    print("**********")
    print(f"Command: {funcName}")
    print(f"Author: {ctx.message.author}")
    print(f"Channel: {ctx.message.channel}")
    print(f"Message: {ctx.message.content}")
    print(f'Custom message: {msg}')

def updateDB(user):
    with open("src/db/strike_users.json") as writeJSON:
        db = json.load(writeJSON)
        user_db = db

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
