from discord.ext import commands

class Test:
	"""Test class for plugin commands"""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context = True)
	async def testes(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("Test no subcommand.")

	@testes.command(pass_context = True)
	async def testicles(self, ctx):
		await ctx.send("TESTICLES!!!!!")

def setup(bot):
	bot.add_cog(Test(bot))