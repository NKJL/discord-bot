import asyncio
import youtube_dl
import discord

from discord.ext import commands
from discord.utils import get

ADMIN_ID = "449356221040820235"             # Role ID for admin
EVERYONE_ID = "191048044706398208"          # Role ID for @everyone
ADMIN_PERMISSIONS_VALUE = "2080898303"      # Permission value in beg-bug for admin

vc = None
audio_controller = None
lock = False

class Audio:
	"""Audio plugin to play Youtube links."""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context = True)
	async def audio(self, ctx):
		"""audio players"""
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid subcommand.")

	@audio.command(pass_context = True)
	async def connect(self, ctx, target = None):
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

	@audio.command(pass_context = True)
	async def play(self, ctx, url):
		"""plays given Youtube url"""
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

	@audio.command(pass_context = True)
	async def pause(self, ctx):
		"""pauses audio"""
		global vc
		global audio_controller
		author = ctx.message.author

		if audio_controller is not None:
			if author is not audio_controller and lock:
				await ctx.send("Controls are locked.")
				return

		if vc is None or not vc.is_playing():
			await ctx.send("Nothing is playing.")
			return
		vc.pause()

	@audio.command(pass_context = True)
	async def resume(self, ctx):
		"""resumes audio"""
		global vc
		global audio_controller
		author = ctx.message.author

		if audio_controller is not None:
			if author is not audio_controller and lock:
				await ctx.send("Controls are locked.")
				return

		if vc is None or not vc.is_paused():
			await ctx.send("Nothing is paused.")
			return
		vc.resume()

	@audio.command(pass_context = True)
	async def stop(self, ctx):
		"""stops playing"""
		global vc
		global audio_controller
		author = ctx.message.author

		if audio_controller is not None:
			if author is not audio_controller and lock:
				await ctx.send("Controls are locked.")
				return

		if vc is None and not vc.is_playing():
			await ctx.send("Nothing is playing.")
			return
		vc.stop()

	@audio.command(pass_context = True)
	async def volume(self, ctx, vol):
		"""adjusts volume between 0 to 10 inclusive"""
		global vc
		global audio_controller
		author = ctx.message.author
		top_id = author.top_role.id

		if int(vol) > 10 or int(vol) < 0:
			await ctx.send("Please enter a number between 0 and 10")
			return

		if audio_controller is not None:
			if str(top_id) != ADMIN_ID and (author is not audio_controller):
				await ctx.send("Someone else is controlling the bot's audio at the moment.")
				return

		if not vc.is_playing or not vc.is_paused:
			await ctx.send("Nothing is playing or paused.")
			return
		
		vc.source.volume = int(vol) / 10

	@audio.command(pass_context = True)
	async def dc(self, ctx):
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
		vc = None
		audio_controller = None
		await ctx.send("Disconnected voice client.")

	@audio.command(pass_context = True)
	async def forcedc(self, ctx):
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
			vc = None
			audio_controller = None
			await ctx.send("Disconnected voice client.")

	@audio.command(pass_context = True)
	async def lock(self, ctx):
		"""locks control of audio to audio_controller and admin"""
		global lock
		lock = True
		author = ctx.message.author
		top_id = author.top_role.id

		if audio_controller is not None:
			if str(top_id) != ADMIN_ID and (author is not audio_controller):
				await ctx.send("Only the person who summoned the bot or an admin can lock the controls.")
				return
		else:
			await ctx.send("No one is controlling audio at the moment.")
			return

		await ctx.send("Audio locked to controller and admin.")

	@audio.command(pass_context = True)
	async def unlock(self, ctx):
		"""unlocks control of audio"""
		global lock
		lock = False
		author = ctx.message.author
		top_id = author.top_role.id

		if audio_controller is not None:
			if str(top_id) != ADMIN_ID and (author is not audio_controller):
				await ctx.send("Only the person who summoned the bot or an admin can unlock the controls.")
				return
		else:
			await ctx.send("No one is controlling audio at the moment.")
			return

		await ctx.send("Audio unlocked for everyone.")

def setup(bot):
	bot.add_cog(Audio(bot))
