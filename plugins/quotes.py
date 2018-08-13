import discord
import json
import datetime as dt
import random

from discord.ext import commands

ADMIN_ID = "449356221040820235"             # Role ID for admin

class Quotes:
	"""Quotes engine"""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context = True)
	async def quotes(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid subcommand.")

	@quotes.command(pass_context = True)
	async def add(self, ctx, user : discord.Member = None, quote = None):
		"""Adds quote to user database"""
		if quote is None or (not isinstance(quote, str)):
			await ctx.send("Enter valid quote string (in quotes).") 
			return
		iterator = ctx.message.channel.history(limit = 10, before = ctx.message)
		time = None
		count = 0
		found = False
		while count < 10:
			msg = await iterator.next()
			# print(msg)
			if msg.content == quote:
				found = True
				time = msg.created_at
				break
			count += 1
		# prev_content = [x.content for x in prev_msgs]
		if not found:
			await ctx.send("Couldn't find quote in previous 10 messages, did you copy it correctly?")
			return

		data = load_json()
		username = user.name
		if username not in data:
			data[username] = []
		index = len(data[username])
		data[username].append({'content' : quote, 'time' : str(time), 'index': index})
		write_json(data)
		await ctx.send("Added to data file.")

	@quotes.command(pass_context = True)
	async def fadd(self, ctx, user : discord.Member = None, quote = None):
		"""Force adds quote to user database"""
		if quote is None or (not isinstance(quote, str)):
			await ctx.send("Enter valid quote string (in quotes).") 
			return
		
		data = load_json()
		username = user.name
		if username not in data:
			data[username] = []
		index = len(data[username])
		data[username].append({'content' : quote, 'time' : str(dt.datetime.now()), 'index': index})
		write_json(data)
		await ctx.send("Added to data file.")

	@quotes.command(pass_context = True)
	async def quote(self, ctx, user : discord.Member = None, index = None):
		"""Finds a random quote by user"""
		if user is None:
			await ctx.send("Enter valid user (mention).")
		data = load_json()
		username = user.name
		if username not in data:
			await ctx.send("No data for mentioned user.")
			return
		quote_list = data[username]
		quoted = None
		if index is None:
			quoted = quote_list[random.randint(0, len(quote_list) - 1)]
		else:
			quoted = quote_list[int(index)]
		content = quoted['content']
		quote_date = quoted['time'].split()[0]
		await ctx.send(f"On {quote_date}, {username} sent\n```{content}```")

	@quotes.command(pass_context = True)
	async def reqquotes(self, ctx, user : discord.Member):
		"""DMs author a list of quotes by user"""
		author = ctx.message.author
		if user is None:
			await ctx.send("Enter valid user (mention).")
		data = load_json()
		username = user.name
		if username not in data:
			await ctx.send("No data for mentioned user.")
			return
		quote_list = data[username]

		await author.send("```" + str(quote_list) + "```")
		await ctx.send("Quote list sent.")

	@quotes.command(pass_context = True)
	async def init(self, ctx):
		author = ctx.message.author
		top_id = author.top_role.id

		if str(top_id) != ADMIN_ID:
			await ctx.send("You don't have permission to do this.")
			return
		data = {}
		with open('data.json', 'w') as f:
			json.dump(data, f)
		await ctx.send("Created json data file.")

def load_json():
	"""Loads json data file and returns data"""
	data = None
	with open('data.json') as f:
		data = json.load(f)
	return data

def write_json(data):
	"""Writes to json data file"""
	with open('data.json', 'w') as f:
		json.dump(data, f, indent = 4)

def setup(bot):
	bot.add_cog(Quotes(bot))

