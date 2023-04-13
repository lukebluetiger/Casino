import discord
from discord.ext import commands
import random

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
async def balance(ctx):
    # Check if the user has a balance in the dictionary
    if ctx.author.id in user_money:
        await ctx.send(f'Your current balance is ${user_money[ctx.author.id]:,.2f}')
    else:
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
        hand = []
        for card in range(0, 2):
            card = self.cards[random.randint(0, len(self.cards)-1)]
            self.cards.remove(card)
            hand.append(card)
        return hand

    def round(self, bet):
        self.pot += bet
        self.money -= bet
        round_card = self.cards[random.randint(0, len(self.cards)-1)]
        self.table.append(round_card)
        self.cards.remove(round_card)

    async def winner(self, ctx):
        score = 0
        bot_score = 0
        values = []
        bot_values = []
        for card in self.hand:
            values.append(self.value[card])
        for card in self.bot_hand:
            bot_values.append(self.value[card])
        self.hand.extend(self.table)
        self.bot_hand.extend(self.table)
        for card in self.hand:
            for i in range(0, len(self.hand)-1):
                if self.value[card] == self.value[(self.hand[(len(self.hand)-1)-i])]:
                    score += 1
                    self.hand.remove(card)
        for card in self.bot_hand:
            for i in range(0, len(self.bot_hand)-1):
                if self.value[card] == self.value[(self.bot_hand[(len(self.bot_hand)-1)-i])]:
                    bot_score += 1
                    self.bot_hand.remove(card)

        if score == bot_score:
            if max(values) > max(bot_values):
                await ctx.send(f"Tie! You win ${self.pot:,.2f} with the higher card. Your current balance is ${self.money:,.2f}.")
            else:
                await ctx.send(f"Tie! The bot wins with the higher card. You lose ${self.pot:,.2f} Your current balance is ${self.money:,.2f}.")
        elif score > bot_score:
            await ctx.send(f"Winner! You win ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        elif score < bot_score:
            await ctx.send(f"You lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
        user_money[ctx.author.id] = self.money
        self.game_start == False

    @commands.command(name='poker')
    async def poker(self, ctx, *, game_handler):
        # detect the command
        if game_handler == "start":
            self.game_start = True
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
            # random card from deck
            # when we take a card from a deck, we are removing the card
            self.hand = self.deal()
            self.bot_hand = self.deal()
            await ctx.send("Your cards are `{}` and `{}`. What would you like to do?".format(self.hand[0], self.hand[1]))

        elif "bet" in game_handler:
            bet_amount = int(game_handler.lstrip("bet "))
            if bet_amount > self.money:
                await ctx.send("Bet higher than current balance, please try again.")
                return
            else:
                if self.round_num == 1:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} add to the pot.")
                    await ctx.send("Table: `{}`".format(self.table[0]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    self.round_num += 1
                elif self.round_num == 2:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} add to the pot.")
                    await ctx.send("Table: `{}` `{}`".format(self.table[0], self.table[1]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    self.round_num += 1
                elif self.round_num == 3:
                    self.round(bet_amount)
                    await ctx.send(f"${bet_amount:,.2f} add to the pot.")
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

    def values(self, hand):
        hand_values = []
        for card in hand:
            hand_values.append(self.value[card])
        return hand_values

    def hit(self):
        card = self.cards[random.randint(0, len(self.cards)-1)]
        self.hand.append(card)
        self.hand_values.append(self.value[card])
        self.cards.remove(card)

    def round(self, bet):
        self.pot += bet
        self.money -= bet

    async def winner(self, ctx):
        score = 0
        bot_score = 0
        values = []
        bot_values = []
        for card in self.hand:
            values.append(self.value[card])
        for card in self.bot_hand:
            bot_values.append(self.value[card])
        self.hand.extend(self.table)
        self.bot_hand.extend(self.table)
        for card in self.hand:
            for i in range(0, len(self.hand)-1):
                if self.value[card] == self.value[(self.hand[(len(self.hand)-1)-i])]:
                    score += self.value[card]
                    self.hand.remove(card)
        for card in self.bot_hand:
            for i in range(0, len(self.bot_hand)-1):
                if self.value[card] == self.value[(self.bot_hand[(len(self.bot_hand)-1)-i])]:
                    bot_score += self.value[card]
                    self.bot_hand.remove(card)

        if score == bot_score:
            if max(values) > max(bot_values):
                winner = True
            else:
                winner = False
        elif score > bot_score:
            winner = True
        elif score < bot_score:
            winner = False

        return winner

    @commands.command(name='blackjack')
    async def blackjack(self, ctx, *, game_handler):
        # detect the command
        if "start" in game_handler:
            self.game_start = True
            bet_amount = int(game_handler.lstrip("start "))
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
            # random card from deck
            # when we take a card from a deck, we are removing the card
            self.hand = self.deal()
            self.bot_hand = self.deal()
            self.hand_values = self.values(self.hand)
            self.pot += bet_amount
            self.money -= bet_amount
            await ctx.send(f"${bet_amount:,.2f} add to the pot.")
            await ctx.send("Dealer: ` ` `{}`".format(self.bot_hand[1]))
            await ctx.send("Hand: `{}` `{}`. What would you like to do?".format(self.hand[0], self.hand[1]))

        elif game_handler == "hit":
            self.hit()
            await ctx.send("Dealer: `  ` `{}`".format(self.bot_hand[1]))
            if sum(self.hand_values) == 21:
                await self.winner()
            if len(self.hand) == 3:
                await ctx.send("Hand: `{}` `{}` `{}`. What would you like to do?".format(self.hand[0], self.hand[1], self.hand[2]))
            if len(self.hand) == 4:
                await ctx.send("Hand: `{}` `{}` `{}` `{}`. What would you like to do?".format(self.hand[0], self.hand[1], self.hand[2], self.hand[3]))

        elif game_handler == "stand":
            await ctx.send("Dealer: `{}` `{}`".format(self.bot_hand[0], self.bot_hand[1]))

        elif game_handler == "fold":
            await ctx.send(f"Folded. Lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
            user_money[ctx.author.id] = self.money
            self.game_start == False

        elif game_handler == "help":
            await ctx.send("`\n start - starts the game \n bet (amount) - bets amount of money \n check - equal to betting 0 \n fold - folds the for the current game \n rules - displays the rules for the game`")

        elif game_handler == "rules":
            await ctx.send("`\n This version of Poker is played against a bot. The player is given a hand and given a choice to bet or fold each round. Each round a new card will be placed on the table. Once the third card is placed, the game is over and the person with the most pairs wins. Aces are equal to 1 in this version.`")


@ client.command()
async def gamba(ctx, *, gambaamount=10):
    for messagecount in range(0, gambaamount):
        await ctx.send("GAMBA ")


client.run(
    token.read())
