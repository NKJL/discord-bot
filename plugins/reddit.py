import praw
import pandas as pd
import datetime as dt
import discord

from . import keys
from discord.ext import commands

reddit = praw.Reddit(client_id = keys.key_14, \
                     client_secret = keys.key_27, \
                     user_agent='fig-bot', \
                     username = keys.reddit_username, \
                     password = keys.reddit_pw)

destiny = reddit.subreddit("DestinyTheGame")

class Reddit:
	"""Plugin for retrieving info from reddit."""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context = True)
	async def reddit(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid subcommand.")

	@reddit.command(pass_context = True)
	async def d2w(self, ctx):
		global destiny

		date = '[' + str(dt.datetime.now()).split()[0] + ']'
		weeklies = list(destiny.search(f'[D2] Weekly Reset Thread', time_filter = 'week'))
		body = weeklies[0].selftext
		await ctx.send("```md\n" + body[0:(len(body) // 2)] + "```")
		await ctx.send("```md\n" + body[(len(body) // 2):(len(body) + 1)] + "```")

	@reddit.command(pass_context = True)
	async def d2d(self, ctx):
		global destiny

		date = '[' + str(dt.datetime.now()).split()[0] + ']'
		dailies = list(destiny.search(f'[D2] Daily Reset Thread', time_filter = 'day'))
		body = dailies[0].selftext
		await ctx.send("```md\n" + body[0 : (len(body) // 3)] + "```")
		await ctx.send("```md\n" + body[(len(body) // 3) : ((len(body) // 3) * 2) + 1] + "```")
		await ctx.send("```md\n" + body[((len(body) // 3) * 2) + 1 : len(body) + 1] + "```")

def setup(bot):
	bot.add_cog(Reddit(bot))