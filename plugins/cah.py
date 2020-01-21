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
    
    def replace(self, card_ind, replace_card):
        return_card = self.cards[card_ind]
        self.cards[card_ind] = replace_card
        return return_card
    
class Player:
    
    def __init__(self, hand, player_id):
        self.hand = hand
        self.player_id = player_id
        self.points = 0

class Game:
    
    def __init__(self, max_score, players, included_packs):
        
        # 0: not in progress
        # 1: waiting for submissions
        # 2: judging
        # 3: polling for players
        # 4: Winner
        self.game_state = 0
        self.max_score = int(max_score)
        self.white_set = CAHSet(100000, "white")
        self.black_set = CAHSet(10000, "black")
        self.player_list = players
        
        self.submissions = {}
        self.submitted = set()
        
        for pack in included_packs:
            self.white_set.add(cahcards.packs[int(pack)][0])
            self.black_set.add(cahcards.packs[int(pack)][1])
            
        self.players = {}
        for player in players:
            self.players[player] = Player(CAHSet(7, "white"), player)
            
        for player in self.players:
            new_hand = []
            
            for i in range(7):
                rand_card = random.choice(self.white_set.cards)
                while rand_card in new_hand:
                    rand_card = random.choice(self.white_set.cards)
                new_hand.append(rand_card)
                           
            self.players[player].hand.add(new_hand)
        
        self.curr_prompt = random.choice(self.black_set.cards)
        self.judge_ind = 0
        
        self.game_state = 1
            
    def new_prompt(self):
        self.curr_prompt = random.choice(self.black_set.cards)
        
    def get_judge(self):
        return self.player_list[self.judge_ind]
            
    def player_submit(self, playerid, card_ind):
        if not playerid in self.submitted and not playerid == self.player_list[self.judge_ind]:
            replace_card = random.choice(self.white_set.cards)
            while replace_card in self.players[playerid].hand.cards:
                replace_card = random.choice(self.white_set.cards)
            
            self.submissions[playerid] = self.players[playerid].hand.replace(card_ind, replace_card)
            self.submitted.add(playerid)
            
            if len(self.submitted) == len(self.players) - 1:
                self.game_state = 2
            return 1
        return 0

    def judge_display(self):
        self.player_indices = [""] * len(self.players)
        index = 1
        return_string = ""
        for player in self.submissions:
            return_string += str(index) + ". " + self.submissions[player] + "\n"
            self.player_indices[index] = player
        return return_string        

    def judge_decision(self, player_index, playerid):
        if playerid == self.player_list[self.judge_ind]:
            
            winning_player = self.players[self.player_indices[player_index]]
            winning_player.points += 1
            
            if winning_player.points >= self.max_score:
                self.game_state = 4
            else:    
                self.judge_ind = (self.judge_ind + 1) % len(player_list)
                self.curr_prompt = random.choice(self.black_set.cards)
                self.game_state = 1
                self.submitted = set()
                self.submissions = {}
            
            return winning_player


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
            await ctx.send("Game already in progress.")
        else:
            self.game = Game(max_score, players[1:len(players) - 1].split(','), packs[1:len(packs) - 1].split(','))
            await ctx.send(self.game.curr_prompt)
            await ctx.send("The judge for this round is: " + self.game.get_judge())
            
    @cah.command(pass_context = True)
    async def submit(self, ctx, card_ind):
        if self.game.game_state == 1:
            
            playerid = str(ctx.message.author.id)
            if self.game.player_submit(playerid, int(card_ind)):
                await ctx.send("Submitted!")
            else:
                await ctx.send("Failed! You are the judge or have already submitted.")

            if self.game.game_state == 2:
                await ctx.send("All players have submitted!")
                await ctx.send("The judge for this round is: " + self.game.get_judge() + "\nPlease enter the number of the winning submission" )
                await ctx.send(self.game.judge_display())
        else:
            await ctx.send("Fuck u")
            
    @cah.command(pass_context = True)
    async def judge(self, ctx, player_index):
        if self.game.game_state == 2:
            playerid = str(ctx.message.author.id)
            winner = self.game.judge_decision(int(player_index), playerid)
            if self.game.game_state == 4:
                await ctx.send(winner.player_id + " has won! Everyone else sucks ass")
                self.game = None
            else:
                await ctx.send(winner.player_id + " has won the round!")
                await ctx.send(self.game.curr_prompt)
                await ctx.send("The judge for this round is: " + self.game.get_judge())
        else:
            await ctx.send("Please make sure you are the judge and it is time to decide the winner.")
            
def setup(bot):
    bot.add_cog(Cah(bot))
