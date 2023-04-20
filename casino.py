import discord
from discord.ext import commands
import random
import time

token = open('C:/Users/Luke/Documents/casino/token.txt')

client = commands.Bot(
    command_prefix='!', intents=discord.Intents.all(), )  # v2
# Define a dictionary to keep track of the money values for each user
user_money = {}


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.add_cog(Poker(bot=client))
    await client.add_cog(Blackjack(bot=client))


@client.command()
async def balance(ctx, user: discord.Member = None):
    # Check if the user has a balance in the dictionary
    if user:  # checks if there was a user in command
        if user.id in user_money:  # checks if user is in dictionary
            await ctx.send(f"{user.mention}'s current balance is ${user_money[user.id]:,.2f}")
        else:
            # otherwise give a balance to user
            user_money[user.id] = 2500.00
            await ctx.send(f"{user.mention}'s current balance is ${user_money[user.id]:,.2f}")
    else:
        if ctx.author.id in user_money:
            await ctx.send(f'Your current balance is ${user_money[ctx.author.id]:,.2f}')
        else:
            # otherwise give a balance
            user_money[ctx.author.id] = 2500.00
            await ctx.send(f'Your current balance is ${user_money[ctx.author.id]:,.2f}')


@client.command()
async def give(ctx, user: discord.Member, amount: float):
    # Check if the sender has enough money to give
    if ctx.author.id not in user_money or user_money[ctx.author.id] < amount:
        await ctx.send('You do not have enough money to give.')
        return

    # Subtract the given amount from the sender's balance and add it to the recipient's balance
    user_money[ctx.author.id] -= amount
    if user.id in user_money:
        user_money[user.id] += amount
    else:
        user_money[user.id] = amount

    await ctx.send(f'{ctx.author.mention} gave {user.mention} ${amount:,.2f}')


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

    def round(self, bet):
        self.pot += bet
        self.money -= bet  # simple money handling for each round
        round_card = self.cards[random.randint(
            0, len(self.cards)-1)]  # pick our round card
        self.table.append(round_card)
        self.cards.remove(round_card)

    async def winner(self, ctx):
        score = 0
        bot_score = 0
        values = []
        bot_values = []
        # since our table cards are technically included in our hands
        self.hand.extend(self.table)
        self.bot_hand.extend(self.table)
        for card in self.hand:
            values.append(self.value[card])  # get values of our cards
        for card in self.bot_hand:
            bot_values.append(self.value[card])
        for card in self.hand:  # check each card in hand
            for i in range(0, len(self.hand)-1):
                # this will check each value against the value of the reversed hand
                if self.value[card] == self.value[(self.hand[(len(self.hand)-1)-i])]:
                    score += 1
                    self.hand.remove(card)
        for card in self.bot_hand:
            for i in range(0, len(self.bot_hand)-1):
                if self.value[card] == self.value[(self.bot_hand[(len(self.bot_hand)-1)-i])]:
                    bot_score += 1
                    self.bot_hand.remove(card)

        if score == bot_score:  # ties
            if max(values) > max(bot_values):  # for higher card
                self.money += self.pot
                await ctx.send(f"Tie! You win ${self.pot:,.2f} with the higher card. Your current balance is ${self.money:,.2f}.")
            else:  # means bot has higher card
                await ctx.send(f"Tie! The bot wins with the higher card. You lose ${self.pot:,.2f} Your current balance is ${self.money:,.2f}.")
        elif score > bot_score:  # should mean this person has more pairs
            self.money += self.pot
            await ctx.send(f"Winner! You win ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        elif score < bot_score:
            await ctx.send(f"You lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        user_money[ctx.author.id] = self.money
        self.game_start == False

    @commands.command(name='poker')
    async def poker(self, ctx, *, game_handler):
        # detect the command
        if game_handler == "start" and not self.game_start:
            self.game_start = True
            self.game = []
            self.pot = 0
            self.round_num = 1
            if ctx.author.id not in user_money:  # from our 'balance' command
                user_money[ctx.author.id] = 2500.00
            self.money = user_money[ctx.author.id]
            self.cards = ["♠️A", "♠️2", "♠️3", "♠️4", "♠️5", "♠️6", "♠️7", "♠️8", "♠️9", "♠️10", "♠️J", "♠️Q", "♠️K",
                          "♥️A", "♥️2", "♥️3", "♥️4", "♥️5", "♥️6", "♥️7", "♥️8", "♥️9", "♥️10", "♥️J", "♥️Q", "♥️K",
                          "♦️A", "♦️2", "♦️3", "♦️4", "♦️5", "♦️6", "♦️7", "♦️8", "♦️9", "♦️10", "♦️J", "♦️Q", "♦️K",
                          "♣️A", "♣️2", "♣️3", "♣️4", "♣️5", "♣️6", "♣️7", "♣️8", "♣️9", "♣️10", "♣️J", "♣️Q", "♣️K"]
            self.table = []
            self.hand = []
            self.bot_hand = []
            if len(self.game) == 0:
                self.game.append(ctx.author)
                await ctx.send("{}/8 players. User !poker join to join. {}, use !poker start to start!".format(len(self.game),self.game[0].mention)) # for our start
            
            elif len(self.game) == 1:
                self.hand = self.deal()
                self.bot_hand = self.deal()
                await ctx.send("Your cards are `{}` and `{}`. What would you like to do?".format(self.hand[0], self.hand[1]))
            
            elif len(self.game) > 1 and len(self.game) < 8:
                self.game.append(ctx.author)
                await ctx.send("{}/8 players. User !poker join to join. {}, use !poker start to start!".format(len(self.game),self.game[0].mention))
            else:
                await ctx.send("Too many players!")
        
        elif game_handler == "join":
            if ctx.author not in self.game:
                self.game.append(ctx.author)
                await ctx.send("{} joined the game!".format(ctx.author.mention))
            else:
                await ctx.send("Already in the game!")
        
        elif game_handler == "start" and ctx.author==self.game[0]:
            game = {}
            for player in self.game:
                game[player] = self.deal() # assign each player in dictionary a hand
                await player.send("Your cards are `{}` and `{}`.".format(game[player][0], game[player][1])) # DM our cards so they are hidden
            await ctx.send("Cards have been selected. Check your DMs for your hand.")

        elif "bet" in game_handler:
            bet_amount = int(game_handler.lstrip("bet "))
            if bet_amount > self.money:  # prevent people from betting too much
                await ctx.send("Bet higher than current balance, please try again.")
                return
            else:
                if self.round_num == 1:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} added to the pot.")
                    await ctx.send("Table: `{}`".format(self.table[0]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    self.round_num += 1
                elif self.round_num == 2:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} added to the pot.")
                    await ctx.send("Table: `{}` `{}`".format(self.table[0], self.table[1]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    self.round_num += 1
                elif self.round_num == 3:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} added to the pot.")
                    await ctx.send("Table: `{}` `{}` `{}`".format(self.table[0], self.table[1], self.table[2]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    await ctx.send("Bot's hand: `{}` `{}`".format(self.bot_hand[0], self.bot_hand[1]))
                    await self.winner(ctx)

        elif game_handler == "fold":
            await ctx.send(f"Folded. Lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
            user_money[ctx.author.id] = self.money
            self.game_start == False

        elif game_handler == "help":
            await ctx.send("`\n start - starts the game \n bet (amount) - bets amount of money \n check - equal to betting 0 \n fold - folds the for the current game \n rules - displays the rules for the game`")

        elif game_handler == "rules":
            await ctx.send("`\n This version of Poker is played against a bot. The player is given a hand and given a choice to bet or fold each round. Each round a new card will be placed on the table. Once the third card is placed, the game is over and the person with the most pairs wins. Aces are equal to 1 in this version.`")


class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # the values for blackjack
        self.value = {"♠️A": 1, "♠️2": 2, "♠️3": 3, "♠️4": 4, "♠️5": 5, "♠️6": 6, "♠️7": 7, "♠️8": 8, "♠️9": 9, "♠️10": 10, "♠️J": 10, "♠️K": 10, "♠️Q": 10,
                      "♥️A": 1, "♥️2": 2, "♥️3": 3, "♥️4": 4, "♥️5": 5, "♥️6": 6, "♥️7": 7, "♥️8": 8, "♥️9": 9, "♥️10": 10, "♥️J": 10, "♥️K": 10, "♥️Q": 10,
                      "♦️A": 1, "♦️2": 2, "♦️3": 3, "♦️4": 4, "♦️5": 5, "♦️6": 6, "♦️7": 7, "♦️8": 8, "♦️9": 9, "♦️10": 10, "♦️J": 10, "♦️K": 10, "♦️Q": 10,
                      "♣️A": 1, "♣️2": 2, "♣️3": 3, "♣️4": 4, "♣️5": 5, "♣️6": 6, "♣️7": 7, "♣️8": 8, "♣️9": 9, "♣️10": 10, "♣️J": 10, "♣️K": 10, "♣️Q": 10}

        self.cards = []  # array of deck of cards
        self.money = 0
        self.pot = 0
        self.round_num = 0
        self.game_start = False

    def deal(self):
        hand = []
        for card in range(0, 2):
            card = self.cards[random.randint(0, len(self.cards)-1)]
            self.cards.remove(card)
            hand.append(card)
        return hand

    def values(self, hand):  # easy way of getting values for someones hand
        hand_values = []
        for card in hand:
            hand_values.append(self.value[card])
        return hand_values

    def hit(self, hand):  # get a card from the deck and add it to given hand
        card = self.cards[random.randint(0, len(self.cards)-1)]
        hand.append(card)
        self.cards.remove(card)
        return hand

    async def winner(self, ctx):
        # reveal our dealer's full hand
        await ctx.send(f"Dealer: `{'` `'.join(self.bot_hand)}`.")
        # how the normal end of a game is played, dealer must hit til above 17
        while sum(self.bot_hand_values) < 17:
            self.bot_hand = self.hit(self.bot_hand)
            self.bot_hand_values = self.values(self.bot_hand)
            await ctx.send(f"Dealer: `{'` `'.join(self.bot_hand)}`.")
        await ctx.send(f"Hand: `{'` `'.join(self.hand)}`.")
        # if dealer busts and player doesn't
        if sum(self.bot_hand_values) > 21 and sum(self.hand_values) < sum(self.bot_hand_values):
            self.pot *= 2
            self.money += self.pot
            await ctx.send(f"Dealer busts! You win ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        elif sum(self.hand_values) <= 21 and (21 - sum(self.hand_values)) < (21 - sum(self.bot_hand_values)):
            self.pot *= 2
            self.money += self.pot
            await ctx.send(f"Winner! You win ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        else:  # since we checked our possible wins already, must mean it is a loss
            await ctx.send(f"You lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        user_money[ctx.author.id] = self.money

    @commands.command(name='blackjack')
    async def blackjack(self, ctx, *, game_handler):
        # detect the command
        if "start" in game_handler:
            self.game_start = True
            try:  # for a default bet
                bet_amount = int(game_handler.lstrip("start "))
            except:
                bet_amount = 100.00
            if ctx.author.id not in user_money:  # from our 'balance' command
                user_money[ctx.author.id] = 2500.00
            self.money = user_money[ctx.author.id]
            self.cards = ["♠️A", "♠️2", "♠️3", "♠️4", "♠️5", "♠️6", "♠️7", "♠️8", "♠️9", "♠️10", "♠️J", "♠️Q", "♠️K",
                          "♥️A", "♥️2", "♥️3", "♥️4", "♥️5", "♥️6", "♥️7", "♥️8", "♥️9", "♥️10", "♥️J", "♥️Q", "♥️K",
                          "♦️A", "♦️2", "♦️3", "♦️4", "♦️5", "♦️6", "♦️7", "♦️8", "♦️9", "♦️10", "♦️J", "♦️Q", "♦️K",
                          "♣️A", "♣️2", "♣️3", "♣️4", "♣️5", "♣️6", "♣️7", "♣️8", "♣️9", "♣️10", "♣️J", "♣️Q", "♣️K"]
            self.table = []
            self.hand = []
            self.hand_values = []
            self.bot_hand = []
            self.pot = 0
            # random card from deck
            # when we take a card from a deck, we are removing the card
            self.hand = self.deal()
            self.bot_hand = self.deal()
            self.hand_values = self.values(self.hand)
            self.bot_hand_values = self.values(self.bot_hand)
            self.pot += bet_amount
            self.money -= bet_amount
            await ctx.send(f"${bet_amount:,.2f} add to the pot.")
            await ctx.send("Dealer: ` ` `{}`".format(self.bot_hand[1]))
            await ctx.send("Hand: `{}` `{}`. What would you like to do?".format(self.hand[0], self.hand[1]))

        elif game_handler == "hit":
            self.hand = self.hit(self.hand)
            # to keep getting our values for each hit
            self.hand_values = self.values(self.hand)
            await ctx.send("Dealer: `  ` `{}`".format(self.bot_hand[1]))
            if sum(self.hand_values) == 21:
                await ctx.send(f"Hand: `{'` `'.join(self.hand)}`.")
                await ctx.send("Blackjack!")
                await self.winner(ctx)
                return
            elif sum(self.hand_values) > 21:
                await ctx.send(f"Hand: `{'` `'.join(self.hand)}`.")
                await ctx.send("Bust!")
                await self.winner(ctx)
                return
            # so we don't have to use different print statements for each card
            await ctx.send(f"Hand: `{'` `'.join(self.hand)}`. What would you like to do?")

        elif game_handler == "stand":
            await self.winner(ctx)

        elif game_handler == "fold":
            await ctx.send(f"Folded. Lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
            user_money[ctx.author.id] = self.money
            self.game_start == False

        elif game_handler == "help":
            await ctx.send("`\n start (amount) - starts the game with bet amount \n  \n fold - folds the for the current game \n rules - displays the rules for the game`")

        elif game_handler == "rules":
            await ctx.send("`\n This version of Blackjack is played against the bot. Players bet in round one with !blackjack start (bet).`")


@ client.command()
async def roulette(ctx, *, bet, bet_amount):
    wheel = {0:'green', 00:'green',1:'red',2:'black',3:'red',4:'black',5:'red',6:'black',7:'red',8:'black',9:'red',10:'black',11:'black',12:'red',13:'black',14:'red',15:'black',16:'red',17:'black',18:'red'
             ,19:'black',20:'black',21:'red',22:'black',23:'red',24:'black',25:'red',26:'black',27:'red',28:'black', 29:'black',30:'red',31:'black',32:'red',33:'black',34:'red',35:'black',36:'red'}

client.run(
    token.read())
