import discord
import random
import asyncio
import unicodedata
import youtube_dl
from discord.ext import commands
from discord.utils import get
from utils import *

ADMIN_ID = "449356221040820235"             # Role ID for admin
EVERYONE_ID = "191048044706398208"          # Role ID for @everyone
ADMIN_PERMISSIONS_VALUE = "2080898303"      # Permission value in beg-bug for admin


bot = commands.Bot(command_prefix = "!", description = "I am a bot.") # Bot
vc = None   # VoiceClient
audio_controller = None # current user controlling audio

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
        await ctx.send("filterp is currently " + filterp)
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
            if filterp == "on":
                if "fuck" in message.content.lower():
                    channel = message.channel
                    await message.add_reaction("\U0001F632")
                    possible_responses = [
                        "This is a hecking Christian server.",
                        "No cursing in this wholesome server you heathen.",
                        "Do you kiss your mother with that mouth?"
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
    await ctx.send(str(member.guild.text_channels))
    channel = discord.utils.get(ctx.guild.text_channels, name = "beg-bug")
    await ctx.send(str(member.permissions_in(channel)))

#
# ADMINISTRATIVE 
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
# MISC. FUNCTIONS
#

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

# @bot.command(pass_context = True)
# async def play(ctx, member, )

@bot.command(pass_context = True)
async def insult(ctx, member : discord.Member = None, tts = None):
    """insults given user with preset insults"""
    try:
        top_id = str(ctx.message.author.top_role.id)
        if top_id == EVERYONE_ID:
            await ctx.send("You need a role to do that.")
            return
        possible_responses = [
            # "I don't speak to idiots",
            # "Fuck you too {0.mention}",
            # "Don't talk to me pussy ass bitch {0.mention}"
            # "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.",
            # "What the fuck did you just fucking type about me, you little bitch? I'll have you know I graduated top of my class at MIT, and I've been involved in numerous secret raids with Anonymous, and I have over 300 confirmed DDoSes. I am trained in online trolling and I'm the top hacker in the entire world. You are nothing to me but just another virus host. I will wipe you the fuck out with precision the likes of which has never been seen before on the Internet, mark my fucking words. You think you can get away with typing that shit to me over the Internet? Think again, fucker. As we chat over IRC I am tracing your IP with my damn bare hands so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your computer. You're fucking dead, kid. I can be anywhere, anytime, and I can hack into your files in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in hacking, but I have access to the entire arsenal of every piece of malware ever created and I will use it to its full extent to wipe your miserable ass off the face of the world wide web, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking fingers. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit code all over you and you will drown in it. You're fucking dead, kiddo."
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


#
# AUDIO FUNCTIONS
#

@bot.group(pass_context = True)
async def music(ctx):
    """music players"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid subcommand.")

@music.command(pass_context = True)
async def connect(ctx, target = None):
    """connects to voice channel of user"""
    try:
        global vc
        global audio_controller
        voice_channel = None
        author = ctx.message.author

        if audio_controller is None:
            audio_controller = author
        else:
            if author is not audio_controller:
                await ctx.send("Someone has already summoned the bot to play audio!")
                return

        if target is None:
            voice_channel = author.voice.channel
        else:
            voice_channel = discord.utils.get(author.guild.voice_channels, name = target)

        if voice_channel is None:
            await ctx.send("Failed to connect to target channel.")
            return

        if vc is not None:
            await vc.disconnect()
        vc = await voice_channel.connect()
        await ctx.send("Connected to voice channel.")
    except:
        await ctx.send("Error.")

@music.command(pass_context = True)
async def play(ctx, url):
    """plays given Youtube url"""
    try:
        global vc
        global audio_controller
        author = ctx.message.author

        if audio_controller is not None:
            if author is not audio_controller:
                await ctx.send("Someone has already summoned the bot to play audio!")
                return
            
        if vc is None:
            await ctx.send("No Voice Client detected.")
            return
        # discord.opus.load_opus('opus')

        # Found on StackOverflow
        opts = {'format': 'bestaudio/best'}
        with youtube_dl.YoutubeDL(opts) as ydl:
            song_info = ydl.extract_info(url, download = False)
        if 'entries' in song_info:
            # Can be a playlist or a list of videos
            video = song_info['entries'][0]
        else:
            # Just a video
            video = song_info 
        # print(video)
        video_url = "youtube.com/watch?v=" + video['id']
        audio_url = video['formats'][0].get('url')
        # print(video['formats'])    

        # vc = await voice_channel.connect()
        options = ["-hq", "-ab 320"]
        vc.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print('done', e))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.2

        # player = await vc.create_ytdl_player(url)
        # player.start()
    except:
        await ctx.send("Error.")

@music.command(pass_context = True)
async def pause(ctx):
    """pauses audio"""
    global vc
    global audio_controller
    author = ctx.message.author

    if audio_controller is not None:
        if author is not audio_controller:
            await ctx.send("Someone has already summoned the bot to play audio!")
            return

    if vc is None or not vc.is_playing():
        await ctx.send("Nothing is playing.")
        return
    vc.pause()

@music.command(pass_context = True)
async def resume(ctx):
    """resumes audio"""
    global vc
    global audio_controller
    author = ctx.message.author

    if audio_controller is not None:
        if author is not audio_controller:
            await ctx.send("Someone has already summoned the bot to play audio!")
            return

    if vc is None or not vc.is_paused():
        await ctx.send("Nothing is paused.")
        return
    vc.resume()

@music.command(pass_context = True)
async def stop(ctx):
    """stops playing"""
    global vc
    global audio_controller
    author = ctx.message.author

    if audio_controller is not None:
        if author is not audio_controller:
            await ctx.send("Someone has already summoned the bot to play audio!")
            return

    if vc is None and not vc.is_playing():
        await ctx.send("Nothing is playing.")
        return
    vc.stop()

@music.command(pass_context = True)
async def volume(ctx, vol):
    """adjusts volume between 0 to 10 inclusive"""
    global vc
    global audio_controller
    author = ctx.message.author
    top_id = author.top_role.id

    if int(vol) > 10 or int(vol) < 0:
        await ctx.send("Please enter a number between 0 and 10")
        return

    if audio_controller is not None:
        if str(top_id) != ADMIN_ID:
            await ctx.send("Someone else is controlling the bot's audio at the moment.")
            return
        if author is not audio_controller:
            await ctx.send("Someone else is controlling the bot's audio at the moment.")
            return

    if not vc.is_playing or not vc.is_paused:
        await ctx.send("Nothing is playing or paused.")
        return
    
    vc.source.volume = int(vol) / 10

@music.command(pass_context = True)
async def dc(ctx):
    """disconnects voice client"""
    global vc
    global audio_controller
    author = ctx.message.author

    if audio_controller is not None:
        if author is not audio_controller:
            await ctx.send("You can't disconnect someone else's audio.")
            return

    if vc is None:
        await ctx.send("Nothing to disconnect.")
        return
    await vc.disconnect()
    await ctx.send("Disconnected voice client.")

@music.command(pass_context = True)
async def forcedc(ctx):
    global vc
    author = ctx.message.author
    top_id = author.top_role.id

    if str(top_id) != ADMIN_ID:
        await ctx.send("You do not have permission to do that.")
        return

    if vc is None:
        await ctx.send("Nothing to disconnect.")
        return
    else:
        await vc.disconnect()
        await ctx.send("Disconnected voice client.")

#
#
#
#

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




