import asyncio
import youtube_dl
import discord
import time

from collections import deque
from discord.ext import commands
from discord.utils import get

ADMIN_ID = "449356221040820235"             # Role ID for admin
EVERYONE_ID = "191048044706398208"          # Role ID for @everyone
ADMIN_PERMISSIONS_VALUE = "2080898303"      # Permission value in beg-bug for admin

player = None

class AudioPlayer:
	"""A PLAYER OF AUDIO"""
	def __init__(self, ctxbot, voice_client, controller, queue):
		self.voice_client = voice_client
		self.audio_controller = controller
		self.queue = queue
		self.lock = False

		self.queue = asyncio.Queue()
		self.next = asyncio.Event()

		self.bot = ctxbot

	# 	bot.loop.create_task(self.player_loop())

	# async def player_loop(self):
	# 	"""Player loop"""
	# 	while not self.bot.is_closed():
	# 		self.next.clear()

	# 		try:
	# 			async with timeout(300):
	# 				source = await self.queue.get()
	# 		except asyncio TimeoutError:
	# 			continue
	# 		self.voice_client.,play(source, after = lambda: self.bot.loop.call_soon_threadsafe(self.next.set()))

	# 		await self.next.wait()


class Audio(commands.Cog):
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
			voice_channel = None
			global player
			author = ctx.message.author

			if player is not None:
				if author is not player.audio_controller:
					await ctx.send("Someone has already summoned the bot to play audio!")
					return
				await player.vc.disconnect()

			if target is None:
				voice_channel = author.voice.channel
			else:
				voice_channel = discord.utils.get(author.guild.voice_channels, name = target)

			if voice_channel is None:
				await ctx.send("Failed to connect to target channel.")
				return

			vc = await voice_channel.connect()
			player = AudioPlayer(vc, author, asyncio.Queue())
			await ctx.send("Connected to voice channel.")
		except:
			await ctx.send("Error.")

	@audio.command(pass_context = True)
	async def play(self, ctx, url = None):
		"""plays given Youtube url"""
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return

		if player.audio_controller is not None:
			if author is not player.audio_controller and player.lock:
				await ctx.send("Someone has already summoned the bot to play audio!")
				return
			
		if url is None:
			if len(player.queue) == 0:
				await ctx.send("Nothing in queue.")
				return
			pass
		else:
			# Found on StackOverflow
			opts = {
			    'format': 'bestaudio/best',
			    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
			    'restrictfilenames': True,
			    'noplaylist': True,
			    'nocheckcertificate': True,
			    'ignoreerrors': False,
			    'logtostderr': False,
			    'no_warnings': True,
			    'default_search': 'auto',
			}

			with youtube_dl.YoutubeDL(opts) as ydl:
				song_info = ydl.extract_info(url, download = False)
			if 'entries' in song_info:
				# Can be a playlist or a list of videos
				video = song_info['entries'][0]
			else:
				# Just a video
				video = song_info 
			if video is None:
				await ctx.send("Failed to acquire audio source.")
				return
			# print(video)
			video_url = "youtube.com/watch?v=" + video['id']
			audio_url = video['url']
			title = video['title']
			duration = video['duration']
			# audio_url = video['url']
			# print(video['formats'])    
			player.queue.appendleft((audio_url, title, duration))

		ffmpeg_options = {
				'before_options': '-nostdin',
				'options': '-vn'
			}

		while (len(player.queue) > 0):
			popped = player.queue.popleft()
			to_play = popped[0]
			title = popped[1]
			duration = int(popped[2])
			vc = player.voice_client
			await ctx.send("Playing:")
			vc.play(discord.FFmpegPCMAudio(to_play, **ffmpeg_options), after=lambda e: print('done', e))
			vc.source = discord.PCMVolumeTransformer(vc.source)
			vc.source.volume = 0.4
			await ctx.send(f"{title}.")

	@audio.command(pass_context = True)
	async def pause(self, ctx):
		"""pauses audio"""
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if not player.voice_client.is_playing():
			await ctx.send("Nothing is playing.")
			return
		if author is not player.audio_controller and player.lock:
			await ctx.send("Controls are locked.")
			return
		player.voice_client.pause()

	@audio.command(pass_context = True)
	async def resume(self, ctx):
		"""resumes audio"""
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if not player.voice_client.is_paused():
			await ctx.send("Nothing is paused.")	
			return
		if author is not player.audio_controller and player.lock:
			await ctx.send("Controls are locked.")
			return
		player.voice_client.resume()

	@audio.command(pass_context = True)
	async def stop(self, ctx):
		"""stops playing"""
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if author is not player.audio_controller and player.lock:
			await ctx.send("Controls are locked.")
			return
		player.voice_client.stop()

	@audio.command(pass_context = True)
	async def volume(self, ctx, vol):
		"""adjusts volume between 0 to 10 inclusive"""
		global player
		author = ctx.message.author
		top_id = author.top_role.id

		if int(vol) > 10 or int(vol) < 0:
			await ctx.send("Please enter a number between 0 and 10")
			return

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if str(top_id) != ADMIN_ID and (author is not player.audio_controller):
			await ctx.send("Someone else is controlling the bot's audio at the moment.")
			return

		if not player.voice_client.is_playing and not player.voice_client.is_paused:
			await ctx.send("Nothing is playing or paused.")
			return
		
		player.voice_client.source.volume = int(vol) / 10

	@audio.command(pass_context = True)
	async def dc(self, ctx):
		"""disconnects voice client"""
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("Nothing to disconnect.")
			return
		if author is not player.audio_controller:
			await ctx.send("You can't disconnect someone else's audio.")
			return

		await player.voice_client.disconnect()
		player = None
		await ctx.send("Disconnected voice client.")

	@audio.command(pass_context = True)
	async def forcedc(self, ctx):
		global player
		author = ctx.message.author
		top_id = author.top_role.id

		if str(top_id) != ADMIN_ID:
			await ctx.send("You do not have permission to do that.")
			return

		if player is None:
			await ctx.send("Nothing to disconnect.")
			return
		else:
			await player.voice_client.disconnect()
			player = None
			await ctx.send("Disconnected voice client.")

	@audio.command(pass_context = True)
	async def add(self, ctx, YT_link = None):
		global player

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if YT_link is None:
			await ctx.send("Please enter a valid YouTube link.")
			return

		opts = {
			    'format': 'bestaudio/best',
			    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
			    'restrictfilenames': True,
			    'noplaylist': True,
			    'nocheckcertificate': True,
			    'ignoreerrors': False,
			    'logtostderr': False,
			    'no_warnings': True,
			    'default_search': 'auto',
			}

		with youtube_dl.YoutubeDL(opts) as ydl:
			song_info = ydl.extract_info(YT_link, download = False)
		if 'entries' in song_info:
			# Can be a playlist or a list of videos
			video = song_info['entries'][0]
		else:
			# Just a video
			video = song_info 
		if video is None:
			await ctx.send("Failed to acquire audio source.")
			return
		video_url = "youtube.com/watch?v=" + video['id']
		title = video['title']
		duration = video['duration']
		audio_url = video['url']
		player.queue.append((audio_url, title, duration))
		await ctx.send(f"Added {title} to queue.")


	@audio.command(pass_context = True)
	async def next(self, ctx):
		global player
		author = ctx.message.author

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return
		if author is not player.audio_controller and player.lock:
			await ctx.send("Controls are locked.")
			return
		if len(player.queue) == 0:
			await ctx.send("Queue is empty.")
			return

		vc = player.voice_client
		if vc.is_playing() or vc.is_paused():
			vc.stop()
		popped = player.queue.popleft()
		to_play = popped[0]

		ffmpeg_options = {
				'before_options': '-nostdin',
				'options': '-vn'
			}

		vc.play(discord.FFmpegPCMAudio(to_play, **ffmpeg_options), after=lambda e: print('done', e))
		vc.source = discord.PCMVolumeTransformer(vc.source)
		vc.source.volume = 0.3

	@audio.command(pass_context = True)
	async def lock(self, ctx):
		"""locks control of audio to audio_controller and admin"""
		global player
		author = ctx.message.author
		top_id = author.top_role.id

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return

		if str(top_id) != ADMIN_ID and (author is not player.audio_controller):
			await ctx.send("Only the person who summoned the bot or an admin can lock the controls.")
			return
		player.lock = True

		await ctx.send("Audio locked to controller and admin.")

	@audio.command(pass_context = True)
	async def unlock(self, ctx):
		"""unlocks control of audio"""
		global player
		author = ctx.message.author
		top_id = author.top_role.id

		if player is None:
			await ctx.send("No VoiceClient detected.")
			return

		if str(top_id) != ADMIN_ID and (author is not player.audio_controller):
			await ctx.send("Only the person who summoned the bot or an admin can lock the controls.")
			return
		player.lock = False

		await ctx.send("Audio unlocked to controller and admin.")

def setup(bot):
	bot.add_cog(Audio(bot))
