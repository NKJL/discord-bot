import discord
import random
import asyncio
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix = "!", description = "I am a bot.")

@bot.command(pass_context = True)
async def addrole(ctx, member: discord.Member = None, to_add: str = None):
    if not str(ctx.message.author.top_role) == "What Is Plagiarism":
        await ctx.send("You do not have permission to do that.")
        return
    if member == None:
        await ctx.send("Please specify a member.")
        return
    if to_add == None:
        await ctx.send("Please specify a role.")
        return
    server = ctx.message.guild
    role = discord.utils.get(server.roles, name = to_add)
    await member.add_roles(role)

@bot.command(pass_context = True)
async def removerole(ctx, member: discord.Member = None, to_remove: str = None):
    if not str(ctx.message.author.top_role) == "What Is Plagiarism":
        await ctx.send("You do not have permission to do that.")
        return
    if member == None:
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

@bot.command(pass_context = True)
async def hello(ctx):
    # we do not want the bot to reply to itself
    await ctx.send("Hello {0.mention}".format(ctx.message.author))

@bot.command(pass_context = True)
async def fuckyoubot(ctx):
    possible_responses = [
        "I don't speak to idiots",
        "Fuck you too {0.mention}",
        "Don't talk to me pussy ass bitch {0.mention}",
        "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.",
        "What the fuck did you just fucking type about me, you little bitch? I'll have you know I graduated top of my class at MIT, and I've been involved in numerous secret raids with Anonymous, and I have over 300 confirmed DDoSes. I am trained in online trolling and I'm the top hacker in the entire world. You are nothing to me but just another virus host. I will wipe you the fuck out with precision the likes of which has never been seen before on the Internet, mark my fucking words. You think you can get away with typing that shit to me over the Internet? Think again, fucker. As we chat over IRC I am tracing your IP with my damn bare hands so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your computer. You're fucking dead, kid. I can be anywhere, anytime, and I can hack into your files in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in hacking, but I have access to the entire arsenal of every piece of malware ever created and I will use it to its full extent to wipe your miserable ass off the face of the world wide web, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking fingers. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit code all over you and you will drown in it. You're fucking dead, kiddo."
        ]
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
    await ctx.send(random.choice(possible_responses).format(ctx.message.author))

@bot.command(pass_context = True)
async def fuckyou(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.message.author
    await ctx.send("Fuck you {0.mention}".format(member))

@bot.command(pass_context = True)
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

bot.run('')