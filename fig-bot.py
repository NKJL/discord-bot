import discord
import asyncio
import unicodedata
import random
import re

from plugins import keys as tokens
from discord.ext import commands
from discord.utils import get
from utils import *
from proflib import * # custom profanity filter list

ADMIN_ID = "449356221040820235"             # Role ID for admin
EVERYONE_ID = "191048044706398208"          # Role ID for @everyone
ADMIN_PERMISSIONS_VALUE = "2080898303"      # Permission value in beg-bug for admin


bot = commands.Bot(command_prefix = "!", description = "I am a bot.") # Bot
bot.remove_command('help')

bot.load_extension('plugins.test')
bot.load_extension('plugins.audio')
bot.load_extension('plugins.reddit')
bot.load_extension('plugins.randchoice')
bot.load_extension('plugins.quotes')

filterp = "off" # tracks profanity filter

@bot.command(pass_context = True)
async def filterswitch(ctx, switch):
    """turns profanity filter on or off"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        global filterp
        if switch != "off" and switch != "on":
            await ctx.send("Specifiy on or off.")
            return
        filterp = switch
        await ctx.send("filter is currently " + filterp)
    except:
        await ctx.send("Error.")

@bot.event
async def on_message(message):
    """reacts based on message content"""
    try:
        global filterp
        if message.content.startswith("!"):
            await bot.process_commands(message)
            return
        if message.author.bot:
            return
        else:
            if filterp == "on":                                 # profanity filter and currently only works on words and not phrases
                to_filter = message.content.lower().split()
                for word in to_filter:
                    if word in profanity_list:
                        channel = message.channel
                        await message.add_reaction("\U0001F632")
                        possible_responses = [
                            "Watch your language!",
                            "Do you kiss your mother with that mouth?",
                            "No dirty words in this wholesome server!"
                        ]
                        await channel.send(random.choice(possible_responses))
            else:
                return
    except:
        await message.channel.send("Error.")

@bot.command(pass_context = True)
async def checkprivilege(ctx, member : discord.Member):
    # await ctx.send("This member has the following roles: " + str(member.roles))
    # await ctx.send("The server has the following roles: " + str(ctx.guild.roles))
    # await ctx.send(str(member.guild.text_channels))
    channel = discord.utils.get(ctx.guild.text_channels, name = "beg-bug")
    await ctx.send(str(member.permissions_in(channel)))

#
#
# ADMINISTRATIVE 
#
#

@bot.command(pass_context = True)
async def addrole(ctx, member : discord.Member, to_add: str = None):
    """add server role to MEMBER"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        if not isinstance(member, discord.Member):
            await ctx.send("Please specify a member.")
            return
        if to_add == None:
            await ctx.send("Please specify a role.")
            return
        server = ctx.message.guild
        role = discord.utils.get(server.roles, name = to_add)
        await member.add_roles(role)
        await ctx.send("Success.")
    except:
        await ctx.send("Error.")

@bot.command(pass_context = True)
async def removerole(ctx, member : discord.Member, to_remove: str = None):
    """remove server role from MEMBER"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        if not isinstance(member, discord.Member):
            await ctx.send("Please specify a member.")
            return
        if to_remove == None:
            await ctx.send("Please specify a role.")
            return
        server = ctx.message.guild
        role = discord.utils.get(server.roles, name = to_remove)
        if discord.utils.get(member.roles, name = to_remove) == None:
            await ctx.send("This member does not have that role.")
            return
        await member.remove_roles(role)
        await ctx.send("Success.")
    except:
        await ctx.send("Error")

@bot.command(pass_context = True)
async def reqrole(ctx, role_name = None):
    """alerts admin that someone requests role"""
    if role_name == None:
        await ctx.send("Please enter the name (in quotes) of the role you would like to receive.")
        return
    member = ctx.message.author
    server = ctx.message.guild
    role = discord.utils.get(server.roles, name = role_name)
    if role == None:
        await ctx.send("Role not found.")
        return
    await member.add_roles(role)
    admin_channel = discord.utils.get(ctx.message.guild.text_channels, name = "bot-test")
    await admin_channel.send(member.name + " has requested the role of " + role_name)

@bot.command(pass_context = True)
async def createvc(ctx, channel_name : str):
    """creates voice channel"""
    try: 
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        channel = await ctx.guild.create_voice_channel(channel_name)
    except:
        await ctx.send("Error. Please try again.")

@bot.command(pass_context = True)
async def deletevc(ctx, channel_name : str):
    """removes voice channel"""
    try: 
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        channel = discord.utils.get(ctx.guild.voice_channels, name = channel_name)
        await channel.delete()
    except:
        await ctx.send("Error. Please try again.") 

@bot.command(pass_context = True)
async def vkick(ctx, member : discord.Member):
    """kicks member from voice channel"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        channel = await ctx.guild.create_voice_channel('kicked')    
        await member.move_to(channel)
        await channel.delete()
        await ctx.send("Successfully kicked {0.name}".format(member))   
    except:
        await ctx.send("Error.")

#
#
# MISC. FUNCTIONS
#
#

@bot.command(pass_context = True)
async def dice(ctx, xdx):
    """dice roll"""
    match = '[1-9]d[1-9][0-9]*'
    match_obj = re.match(match, xdx)
    if match_obj == None:
        await ctx.send("Format your roll like 2d6 or 1d20.")
        return

    num_dice = int(xdx.split('d')[0])
    sides = int(xdx.split('d')[1])
    if sides > 99:
        await ctx.send("Sides cannot exceed 99.")
        return

    roll_values = []
    for i in range(0, num_dice):
        roll_values.append(random.randint(1, sides))

    str_rolls = str(roll_values)
    str_sum = str(sum(roll_values))

    await ctx.send(f"You rolled:\n{str_rolls}\nSum is {str_sum}.")
        

@bot.command(pass_context = True)
async def tts(ctx, message : str, channel : str = None):
    # for c in ctx.message.guild.text_channels:
    #     await ctx.send(c.name)
    try:
        if channel == None:
            await ctx.send(message, tts = 'true')
        else:
            tts_channel = discord.utils.get(ctx.message.guild.text_channels, name = channel)
            if tts_channel == None:
                await ctx.send("Couldn't find channel.", tts = 'true')
            else:
                await tts_channel.send(message, tts = 'true')
    except:
        await ctx.send("Error.")

@bot.command(pass_context = True)
async def hello(ctx):
    # we do not want the bot to reply to itself
    await ctx.send("Hello {0.mention}".format(ctx.message.author))

@bot.command(pass_context = True)
async def fuckyoubot(ctx):
    await ctx.send("Fuck you too!")

@bot.command(pass_context = True)
async def ping(ctx, member : discord.Member, freq = 1):
    """pings user number of times"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if not top_id == ADMIN_ID:
            await ctx.send("You do not have permission to do that.")
            return
        if freq > 10:
            await ctx.send("Select number less than 10")
            return
        for x in range(0, freq):
            await ctx.send("{0.mention}".format(member))
    except:
        await ctx.send("Error.")

@bot.command(pass_context = True)
async def insult(ctx, member : discord.Member = None, tts = None):
    """insults given user with preset insults"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if top_id == EVERYONE_ID:
            await ctx.send("You need a role to do that.")
            return
        possible_responses = []
        a = ['artless', 'bawdy', 'beslubbering', 'bootless', 'churlish', 'cockered', 'clouted', 'craven', 'currish', 'dankish', 'dissembling', 'droning', 'errant', 'fawning', 'fobbing', 'froward', 'frothy', 'gleeking', 'goatish', 'gorbellied', 'impertinent', 'infectious', 'jarring', 'loggerheaded',
            'lumpish', 'mammering', 'mangled', 'mewling', 'paunchy', 'pribbling', 'puking', 'puny', 'qualling', 'rank', 'reeky', 'roguish', 'pruttish', 'saucy', 'spleeny', 'spongy', 'surly', 'tottering', 'unmuzzled', 'vain', 'venomed', 'villainous', 'warped', 'wayward', 'weedy', 'yeasty']
        b = ['base-court', 'bat-fowling', 'beef-witted', 'beetle-headed', 'boil-brained', 'clapper-clawed', 'clay-brained', 'common-kissing', 'crook-pated', 'dismal-dreaming', 'dizzy-eyed', 'doghearted', 'dread-bolted', 'earth-vexing', 'elf-skinned', 'fat-kidneyed', 'fen-sucked', 'flap-mouthed', 'fly-bitten', 'folly-fallen', 'fool-born', 'full-gorged', 'guts-griping', 'half-faced', 'hasty-witted',
            'hedge-born', 'hell-hated', 'idle-headed', 'ill-breeding', 'ill-nurtured', 'knotty-pated', 'milk-livered', 'motley-minded', 'onion-eyed', 'plume-plucked', 'pottle-deep', 'pox-marked', 'reeling-ripe', 'rough-hewn', 'rude-growing', 'rump-fed', 'shard-borne', 'sheep-biting', 'spur-galled', 'swag-bellied', 'tardy-gaited', 'tickle-brained', 'toad-spotted', 'unchin-snouted', 'weather-bitten']
        c = ['apple-john', 'baggage', 'barnacle', 'bladder', 'boar-pig', 'bugbear', 'bum-bailey', 'canker-blossom', 'clack-dish', 'clotpole', 'coxcomb', 'codpiece', 'death-token', 'dewberry', 'flap-dragon', 'flax-wench', 'flirt-gill', 'foot-licker', 'fustilarian', 'giglet', 'gudgeon', 'haggard', 'harpy', 'hedge-pig',
            'horn-beast', 'hugger-mugger', 'joithead', 'lewdster', 'lout', 'maggot-pie', 'malt-worm', 'mammet', 'measle', 'minnow', 'miscreant', 'moldwar', 'mumble-news', 'nut-hook', 'pigeon-egg', 'pignut', 'puttock', 'pumpion', 'ratsbane', 'scut', 'skainsmate', 'strumpet', 'varlot', 'vassal', 'whey-face', 'wagtail']
        for _ in range(3):
            possible_responses.append("{0.mention} is a " + random.choice(a) + " " + random.choice(b) + " " + random.choice(c) + ".")
        for _ in range(3):
            possible_responses.append("{0.mention} has a " + random.choice(a) + " penis.")
        if (tts == None):
            await ctx.send(random.choice(possible_responses).format(member))
        elif (tts == 'tts'):
            await ctx.send( random.choice(possible_responses).format(member), tts = 'yes')
        else:
            await ctx.send("Unknown sub-command")
    except:
        await ctx.send("Error.")


@bot.command(pass_context = True)
# @commands.check(is_admin)
async def test(ctx):
    await ctx.send(str(ctx.message.author.top_role))


@bot.event  
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context = True)
async def add(ctx, 
    left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command(pass_context = True)
async def get_id(ctx, member: discord.Member):
    await ctx.send(member.id)

#
#
#

help_msg = """  ``` 
AUDIO
----------
!audio connect    
!audio connect <channel name in quotes> 
!audio play <YouTube link> 
!audio pause
!audio resume
!audio stop
!audio add <YouTube link>
!audio next
!audio dc 
!audio lock 
!audio unlock 
\n
REDDIT
----------
!reddit d2w
!reddit d2d
\n
RANDCHOICE
----------
!randchoice setup <number = 1>
!randchoice add <option>
!randchoice select
\n
MISC
----------
!reqrole <role name>
!dice
!tts <message in quotes> <channel in quotes> 
!insult <@member> 
!insult <@member> tts
!hello
!fuckyoubot
\n
ADMIN
----------
!addrole <@member> <role name in quotes>
!removerole <@member> <role name in quotes>
!createvc <name>
!deletevc <name>
!vkick <@member>
!ping <@member> <frequence < 10>``` \
"""

@bot.command(pass_context = True)
async def help(ctx):
    global help_msg
    await ctx.send(help_msg)
#
#
#

bot.run(tokens.token)




