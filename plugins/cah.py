import praw
import pandas as pd
import datetime as dt
import discord
import random

from . import cahcards
from . import keys
from discord.ext import commands

class CAHSet:
    
    def __init__(self, max_cards, color):
        if color == "black":
            self.color = 1
        else:
            self.color = 0
        self.max_cards = max_cards
        self.card_num = 0
        self.cards = []
        
    def add(self, card_list):
        for card in card_list:
            if self.card_num >= self.max_cards:
                return 0
            else:
                self.cards.append(card)
                self.card_num += 1
        return 1            
    
class Player:
    
    def __init__(self, hand, player_id):
        self.hand = hand
        self.player_id = player_id
        

class Game:
    
    def __init__(self, max_score, players, included_packs):
        
        self.max_score = max_score
        self.white_set = CAHSet(100000, "white")
        self.black_set = CAHSet(10000, "black")
        
        for pack in included_packs:
            self.white_set.add(cahcards.packs[int(pack)][0])
            self.black_set.add(cahcards.packs[int(pack)][1])
            
        self.players = []
        for player in players:
            self.players.append(Player(CAHSet(7, "white"), player))
            
        for player in self.players:
            new_hand = []
            
            for i in range(7):
                rand_card = random.choice(self.white_set.cards)
                while rand_card in new_hand:
                    rand_card = random.choice(self.white_set.cards)
                new_hand.append(rand_card)
                           
            player.hand.add(new_hand)
        

class Cah(commands.Cog):
    """Plugin for retrieving info from reddit."""
    def __init__(self, bot):
        self.bot = bot
        self.game = None

    @commands.group(pass_context = True)
    async def cah(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand.")
            
    @cah.command(pass_context = True)
    async def newgame(self, ctx, max_score, players, packs):
        if self.game:
            await ctx.send("Game already in progress, you homunculus")
        else:
            self.game = Game(max_score, players[1:len(players) - 1].split(), packs[1:len(packs) - 1].split())
            
def setup(bot):
    bot.add_cog(Cah(bot))
