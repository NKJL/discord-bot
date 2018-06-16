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
        "Don't talk to me pussy ass bitch {0.mention}"]
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