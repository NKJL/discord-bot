import discord
import random
from discord.ext import commands

BOT_PREFIX = "!"
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.commands()
async def fuckyoubot():
    possible_responses = [
        "Fuck you too retard",
        "Kill yourself retard ass bitch",
        "I don't talk to subhumans"
        ]
    await client.say(random.choice(possible_responses))
# @bot.command()
# async def add(left : int, right : int):
#     """Adds two numbers together."""
#     await bot.say(left + right)

client.run('NDU2Nzg2MjI2NzQyMTY1NTI3.DgWnxg.puWWaVD1jE67kSRYKOEKwh8SxRk')