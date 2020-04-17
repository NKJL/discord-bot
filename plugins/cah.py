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

    def get_hand(self):
        return self.hand

class Game:
    
    def __init__(self, max_score, included_packs):
        
        # 0: not in progress
        # 1: waiting for submissions
        # 2: judging
        # 3: polling for players
        # 4: Winner
        self.game_state = 0
        self.max_score = int(max_score)
        self.white_set = CAHSet(100000, "white")
        self.black_set = CAHSet(10000, "black")
        self.update = False # <---- indicator to update player list related variables, might not be needed
        # self.player_list = players
        
        self.submissions = {}
        self.submitted = set()
        
        for pack in included_packs:
            self.white_set.add(cahcards.packs[int(pack)][0])
            self.black_set.add(cahcards.packs[int(pack)][1])
            
        self.players = {}
        self.judge_list = []
        # for player in players:
        #     self.players[player] = Player(CAHSet(7, "white"), player)
            
        # for player in self.players:
        #     new_hand = [] 
            
        #     for i in range(10):
        #         rand_card = random.choice(self.white_set.cards)
        #         while rand_card in new_hand:
        #             rand_card = random.choice(self.white_set.cards)
        #         new_hand.append(rand_card)
                           
        #     self.players[player].hand.add(new_hand)
        
        # self.curr_prompt = random.choice(self.black_set.cards)
        self.judge_ind = 0
        
        # self.game_state = 1

    def get_player_obj(self, p_id):
        if p_id in self.players.keys():
            return self.players[p_id][0]
        return None

    def get_member_obj (self, p_id):
        if p_id in self.players.keys():
            return self.players[p_id][1]
        return None

    def get_player_hand(self, p_id):
        if p_id in self.players.keys():
            return get_player_obj(p_id).get_hand()
        return None

    def get_players(self):
        return self.players.keys()

    def start(self):
        player_keys = self.players.keys()
        self.judge_list = list(player_keys)
        for player in player_keys:
            new_hand = [] 
            
            for i in range(10):
                rand_card = random.choice(self.white_set.cards)
                while rand_card in new_hand:
                    rand_card = random.choice(self.white_set.cards)
                new_hand.append(rand_card)
                           
            get_player_hand(player).add(new_hand)

        self.curr_prompt = random.choice(self.black_set.cards)
        self.judge_ind = 0
        self.game_state = 1

    def add_player(self, new_player: discord.Member):
        p_id = new_player.id
        self.players[p_id] = (Player(CAHSet(10, "white"), new_player))
            
    def new_prompt(self):
        self.curr_prompt = random.choice(self.black_set.cards)
        
    def get_judge(self):
        return self.players.keys()[judge_ind]
            
    def player_submit(self, p_id, card_ind):
        if p_id not in self.submitted and p_id in self.players.keys():
            replace_card = random.choice(self.white_set.cards)
            while replace_card in self.players[p_id].hand.cards:
                replace_card = random.choice(self.white_set.cards)
            
            self.submissions[p_id] = self.players[p_id].hand.replace(card_ind, replace_card)
            self.submitted.add(p_id)
            
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

    def judge_decision(self, player_index, p_id):
        if p_id == self.judge_list[self.judge_ind]:
            
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
    def update(self):
        self.update = not self.update

    def get_state(self):
        return self.game_state


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
    async def newgame(self, ctx, max_score, packs):
        if self.game:
            await ctx.send("Game already in progress.")
        else:
            self.game = Game(max_score, packs[1:len(packs) - 1].split(','))
            await ctx.send("Game instance created.")

    @cah.command(pass_context = True)
    async def join(self, ctx):
        if not game:
            await ctx.send("Create a new game first with !newgame")
            return

        new_player = ctx.message.author
        p_id = new_player.id
        if p_id not in self.game.get_players:
            self.game.add_player(new_player)
            if self.game_state() != 0:
                self.game.update()
            await ctx.send(f"{new_player.name} has joined the game!")
        else:
            await ctx.send("You have already joined")

    @cah.command(pass_context = True)
    async def start(self, ctx)
        if not game:
            await ctx.send("Create a new game first with !newgame")
            return
        if len(self.game.get_players) < 3:
            await ctx.send("There are less than 3 players in the lobby.")
            return

        self.game.start()
        ctx.send(f"Prompt:\n {self.game.curr_prompt}")
        judge = self.game.get_players[self.game.get_judge()]

    @cah.command(pass_context = True)
    async def fstart(self, ctx):
        """for testing purposes only"""
        if not game:
            await ctx.send("Create a new game first with !newgame")
            return

        self.game.start()
        ctx.send(f"Prompt:\n {self.game.curr_prompt}")
        judge = self.game.get_players[self.game.get_judge()]

            
    @cah.command(pass_context = True)
    async def submit(self, ctx, card_ind):
        if self.game.game_state == 1:
            
            p_id = ctx.message.author.id
            if self.game.player_submit(p_id, int(card_ind)):
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
            p_id = ctx.message.author.id
            winner = self.game.judge_decision(int(player_index), p_id)
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
