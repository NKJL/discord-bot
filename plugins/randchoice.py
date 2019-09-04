import random
import discord

from discord.ext import commands

class RandChoice(commands.Cog):
	"""Collects user inputs and selects on at random"""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context = True)
	async def randc(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid subcommand.")
			return

	@randc.command(pass_context = True)
	async def setup(self, ctx, max_per_person = 1):
		"""Sets up the selection"""
		global sel_channel
		global user_choices
		global max_choices

		if sel_channel is not None:
			await ctx.send("A selection is in process right now.")
			return
		else:
			sel_channel = ctx.message.channel
			await ctx.send("A selection has been set up.")
		max_choices = max_per_person


	@randc.command(pass_context = True)
	async def add(self, ctx, option):
		"""Adds an option to the selection pool"""
		global sel_channel
		global user_choices
		global max_choices
		global options

		if sel_channel == None:
			await ctx.send("There's no selection going on right now.")
			return
		if not isinstance(option, str):
			await ctx.send("Invalid option.")
			return
		if ctx.message.channel != sel_channel:
			await ctx.send("The selection is in another channel.")
			return
		author = ctx.message.author
		if author.name not in user_choices:
			options.append(option)
			user_choices[author.name] = 1
			await ctx.send(f"Added {option} to pool.")
		elif user_choices[author.name] >= max_choices:
			await ctx.send("{0.mention}, you have reached the maximum number of options.".format(author))
			return
		else:
			options.append(option)
			user_choices[author.name] += 1
			await ctx.send(f"Added {option} to pool.")

	@randc.command(pass_context = True)
	async def select(self, ctx):
		"""Selects one option from options at random"""
		global sel_channel
		global user_choices
		global max_choices
		global options

		num = len(options)
		if num == 0:
			await ctx.send("No options have been added.")
			return
		selection = random.randint(0, num - 1)
		selected = options[selection]
		await ctx.send(f'{selected} has been selected.')
		sel_channel = None	
		user_choices = {}
		options = []
		max_choices = 1

	@randc.command(pass_context = True)
	async def clear(self, ctx):
		"""Clears all variables"""
		global sel_channel
		global user_choices
		global max_choices
		global options

		sel_channel = None	
		user_choices = {}
		options = []
		max_choices = 1

sel_channel = None	
user_choices = {}
options = []
max_choices = 1

def setup(bot):
	bot.add_cog(RandChoice(bot))