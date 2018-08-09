import discord
from discord.utils import get

# utility functions for fig-bot

# returns a list of voice channels of GUILD
def get_voice_channels(guild):
	return guild.voice_channels 

# returns a list of text channels of GUILD
def get_text_channels(guild):
	return guild.text_channels 

