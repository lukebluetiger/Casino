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

value = {"♠️A": 1, "♠️2": 2, "♠️3": 3, "♠️4": 4, "♠️5": 5, "♠️6": 6, "♠️7": 7, "♠️8": 8, "♠️9": 9, "♠️10": 10, "♠️J": 11, "♠️K": 12, "♠️Q": 13,
         "♥️A": 1, "♥️2": 2, "♥️3": 3, "♥️4": 4, "♥️5": 5, "♥️6": 6, "♥️7": 7, "♥️8": 8, "♥️9": 9, "♥️10": 10, "♥️J": 11, "♥️K": 12, "♥️Q": 13,
         "♦️A": 1, "♦️2": 2, "♦️3": 3, "♦️4": 4, "♦️5": 5, "♦️6": 6, "♦️7": 7, "♦️8": 8, "♦️9": 9, "♦️10": 10, "♦️J": 11, "♦️K": 12, "♦️Q": 13,
         "♣️A": 1, "♣️2": 2, "♣️3": 3, "♣️4": 4, "♣️5": 5, "♣️6": 6, "♣️7": 7, "♣️8": 8, "♣️9": 9, "♣️10": 10, "♣️J": 11, "♣️K": 12, "♣️Q": 13}


class Poker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = []  # array of deck of cards
        self.money = 0
        self.pot = 0
        self.round_num = 0
        self.game_start = False

    def deal(self):
        hand = []
        player_card1 = self.cards[random.randint(0, len(self.cards)-1)]
        self.cards.remove(player_card1)
        hand.append(player_card1)
        player_card2 = self.cards[random.randint(0, len(self.cards)-1)]
        self.cards.remove(player_card2)
        hand.append(player_card2)
        return hand

    def round(self, bet):
        self.pot += bet
        self.money -= bet
        round_card = self.cards[random.randint(0, len(self.cards)-1)]
        self.table.append(round_card)
        self.cards.remove(round_card)

    def winner(self):
        score = 0
        bot_score = 0
        values = []
        bot_values = []
        for card in self.hand:
            values.append(value[card])
        for card in self.bot_hand:
            bot_values.append(value[card])
        self.hand.extend(self.table)
        self.bot_hand.extend(self.table)
        for card in self.hand:
            for i in range(0, len(self.hand)-1):
                if value[card] == value[(self.hand[(len(self.hand)-1)-i])]:
                    score += 1
        for card in self.bot_hand:
            for i in range(0, len(self.bot_hand)-1):
                if value[card] == value[(self.bot_hand[(len(self.bot_hand)-1)-i])]:
                    bot_score += 1

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
                    winner = self.winner()
                    await ctx.send("Table: `{}` `{}` `{}`".format(self.table[0], self.table[1], self.table[2]))
                    await ctx.send("Hand: `{}` `{}`".format(self.hand[0], self.hand[1]))
                    await ctx.send("Bot's hand: `{}` `{}`".format(self.bot_hand[0], self.bot_hand[1]))
                    if winner:
                        self.money += self.pot
                        await ctx.send(f"Winner! You win ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
                    else:
                        await ctx.send(f"You lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
                    user_money[ctx.author.id] = self.money
                    self.game_start == False

        elif game_handler == "fold":
            await ctx.send(f"Folded. Lost ${self.pot:,.2f}. Your current balance is ${self.money:,.2f}.")
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
