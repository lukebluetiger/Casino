import discord
from discord.ext import commands
import random
from economy import load, dump

user_money = load()

class Poker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = []  # array of deck of cards
        self.money = 0
        self.pot = 0
        self.round_num = 0
        self.game_start = False
        self.value = {"♠️A": 1, "♠️2": 2, "♠️3": 3, "♠️4": 4, "♠️5": 5, "♠️6": 6, "♠️7": 7, "♠️8": 8, "♠️9": 9, "♠️10": 10, "♠️J": 11, "♠️K": 12, "♠️Q": 13,
                      "♥️A": 1, "♥️2": 2, "♥️3": 3, "♥️4": 4, "♥️5": 5, "♥️6": 6, "♥️7": 7, "♥️8": 8, "♥️9": 9, "♥️10": 10, "♥️J": 11, "♥️K": 12, "♥️Q": 13,
                      "♦️A": 1, "♦️2": 2, "♦️3": 3, "♦️4": 4, "♦️5": 5, "♦️6": 6, "♦️7": 7, "♦️8": 8, "♦️9": 9, "♦️10": 10, "♦️J": 11, "♦️K": 12, "♦️Q": 13,
                      "♣️A": 1, "♣️2": 2, "♣️3": 3, "♣️4": 4, "♣️5": 5, "♣️6": 6, "♣️7": 7, "♣️8": 8, "♣️9": 9, "♣️10": 10, "♣️J": 11, "♣️K": 12, "♣️Q": 13}

    def deal(self):
        hand = []  # empty hand
        for card in range(0, 2):  # for each card pick a random from deck
            card = self.cards[random.randint(0, len(self.cards)-1)]
            self.cards.remove(card)
            hand.append(card)
        return hand

    def bet(self, player, bet):  # simple money handling for each bet
        self.money = user_money[player.id]
        self.money -= bet 
        self.pot += bet
        user_money[player.id] = self.money

    def round(self): 
        round_card = self.cards[random.randint(
            0, len(self.cards)-1)]  # pick our round card
        self.table.append(round_card)
        self.cards.remove(round_card)

    def get_values(cards):
        values = []
        for card in cards:
            values.append[self.value[card]]
        return values
    
    def get_score(values):
        score = 0
        for value in values:  # check each card in hand
            for i in range(0, len(values)-1):
                if value == values[[(len(values)-1)-i]]:
                    score += 1
    
    async def faceoff(self, ctx):
        # since our table cards are technically included in our hands
        self.hand.extend(self.table)
        self.bot_hand.extend(self.table)
        values = self.get_values(self.hand) # get card values
        bot_values = self.get_values(self.bot_hand)
        score = self.get_score(values)
        bot_score = self.get_score(bot_values)
        if score == bot_score:  # ties
            if max(values) > max(bot_values):  # for higher card
                self.money += self.pot
                await ctx.send(f"Tie! You win ${self.pot:,.2f} with the higher card. Your current balance is ${self.money:,.2f}.")
            else:  # means bot has higher card
                await ctx.send(f"Tie! The bot wins with the higher card. You lose ${self.pot:,.2f} Your current balance is ${self.money:,.2f}.")

    async def winner(self, ctx, player):
        self.money += self.pot
        await ctx.send(f"Winner! {player.mention} wins ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        user_money[player.id] = self.money
        self.game_start == False

    async def round1(self, ctx):
        for player in self.players:
            self.game[player] = self.deal() # assign each player in dictionary a hand
            await player.send("Your cards are `{}` and `{}`.".format(self.game[player][0], self.game[player][1])) # DM our cards so they are hidden
        await ctx.send("Cards have been selected. Check your DMs for your hand.")

    @commands.command(name='poker')
    async def poker(self, ctx, *, game_handler):
        # commands that can be used outside a game
        if game_handler == "help":
            return await ctx.send("`\n start - starts the game  \n join - joins the game \n bet (amount) - bets amount of money \n check - equal to betting 0 \n fold - folds the for the current game \n end - must be from the creator of the game, ends the current game \n rules - displays the rules for the game`")
            
        
        if game_handler == "rules":
            return await ctx.send("`\n Each player is given a hand and given a choice to bet or fold each round. Each round a new card will be placed on the table. Once the third card is placed, the game is over and the person with the most pairs wins. Aces are equal to 1 in this version.`")
            
        
        elif not self.game_start: # to confirm there is not a game currently happening 
            if game_handler == "start":
                # initialize the empty values for our start
                self.players = []
                self.game = {}
                self.pot = 0
                self.round_num = 1
                self.bets = []
                self.cards = ["♠️A", "♠️2", "♠️3", "♠️4", "♠️5", "♠️6", "♠️7", "♠️8", "♠️9", "♠️10", "♠️J", "♠️Q", "♠️K",
                            "♥️A", "♥️2", "♥️3", "♥️4", "♥️5", "♥️6", "♥️7", "♥️8", "♥️9", "♥️10", "♥️J", "♥️Q", "♥️K",
                            "♦️A", "♦️2", "♦️3", "♦️4", "♦️5", "♦️6", "♦️7", "♦️8", "♦️9", "♦️10", "♦️J", "♦️Q", "♦️K",
                            "♣️A", "♣️2", "♣️3", "♣️4", "♣️5", "♣️6", "♣️7", "♣️8", "♣️9", "♣️10", "♣️J", "♣️Q", "♣️K"]
                self.table = []
                self.hand = []
                if len(self.players) == 0:
                    self.players.append(ctx.author)
                    self.game_start = True
                    await ctx.send("{}/8 players. Use `!poker join` to join. {}, use `!poker start` to start!".format(len(self.players),self.players[0].mention)) # for our start

            else:
                await ctx.send("You must be in a game to use this command! Use `!poker start` to start!") # else the player is probably trying to use a game specific command while not in a game   
        
        elif self.game_start:
            if len(self.players) == 1:
                await ctx.send("Can't start a game with 1 player!")
            else:
                await ctx.send("Game must be started by {}.".format(self.players[0].name))
                
            if game_handler == "start" and not self.game and ctx.author==self.players[0] and len(self.players) > 1: # confirming that there isn't a game currently going on and the person using 'start' is the one who made the game
                self.round1(ctx)
                for self.round_num in range(1,3):
                    self.round()
                    for player in self.players:
                        if player.id not in user_money:  # from our 'balance' command
                            user_money[player.id] = 2500.00
                        self.money = user_money[player.id]
                        await ctx.send("{} 's turn. What would you like to do?".format(player.mention))
                        def check(m):
                            return m.author == player and "bet" or "fold" in m # confirm this message is our player and they are playing
                        msg = await client.wait_for('message', check=check)

                        if "bet" in msg.content:
                            bet_amount = int(msg.content.lstrip("!poker bet "))
                            if bet_amount > self.money:  # prevent people from betting too much
                                return await ctx.send("Bet higher than current balance, please try again.")
                            self.bet(player, bet_amount)
                            await ctx.send(f"${bet_amount:,.2f} added to the pot.")
                            await ctx.send("Pot: `${}`".format(self.pot))
                            await ctx.send(f"Table: `{'` `'.join(self.table)}`")
                        
                        elif "fold" in msg.content:
                            await ctx.send(f"Folded. Your current balance is ${self.money:,.2f}.")
                            user_money[ctx.author.id] = self.money
                            self.players.remove(player)
                            if len(self.players) == 1:
                                await self.winner(self.players[0])

                
                            

            
            elif game_handler == "join":
                if len(self.players) >= 1 and len(self.players) < 8: # confirm the game doesnt have too many players and they're not in the game
                    self.players.append(ctx.author) # add player to players
                    await ctx.send("{} joined the game!".format(ctx.author.mention))
                    await ctx.send("{}/8 players. Use `!poker join` to join. {}, use `!poker start` to start!".format(len(self.players),self.players[0].mention))
                elif len(self.players) == 8: # max amount of players
                    await ctx.send("Too many players!")
                else:
                    await ctx.send("Already in the game!")

            # elif "bet" in game_handler:
            #     bet_amount = int(game_handler.lstrip("bet "))
            #     if bet_amount > self.money:  # prevent people from betting too much
            #         await ctx.send("Bet higher than current balance, please try again.")
            #         return
            #     else:
            #         if self.round_num == 1:
            #             self.round(bet_amount)
            #             await ctx.send(f"${bet_amount:,.2f} added to the pot.")
            #             await ctx.send("Pot: `{}`".format(self.pot))
            #             await ctx.send("Table: `{}`".format(self.table[0]))
            #             self.round_num += 1
            #         elif self.round_num == 2:
            #             self.round(bet_amount)
            #             await ctx.send(f"${bet_amount:,.2f} added to the pot.")
            #             await ctx.send("Pot: `{}`".format(self.pot))
            #             await ctx.send("Table: `{}`".format(self.table[0]))
            #             self.round_num += 1
            #         elif self.round_num == 3:
            #             self.round(bet_amount)
            #             await ctx.send(f"${bet_amount:,.2f} added to the pot.")
            #             await ctx.send("Pot: `{}`".format(self.pot))
            #             await ctx.send("Table: `{}`".format(self.table[0]))
            #             await self.winner(ctx)

            # elif game_handler == "fold": # a fold
            #     await ctx.send(f"Folded. Lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
            #     user_money[ctx.author.id] = self.money
            
            elif game_handler == "end" and ctx.author == self.players[0]: # a way for the game's creator to end the game
                await ctx.send("Game ended.")
                self.game_start = False
            