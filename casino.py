import discord
from discord.ext import commands
import random
import asyncio

token = open('C:/Users/Luke/Documents/casino/token.txt')

client = commands.Bot(
    command_prefix='!', intents=discord.Intents.all(), )  # v2
# Define a dictionary to keep track of the money values for each user
user_money = {}


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.command()
async def balance(ctx):
    # Check if the user has a balance in the dictionary
    if ctx.author.id in user_money:
        await ctx.send(f'Your current balance is ${user_money[ctx.author.id]:,.2f}')
    else:
        await ctx.send('You do not have a balance yet.')


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

values = {"♠️1": 1, "♠️2": 2, "♠️3": 3, "♠️4": 4, "♠️5": 5, "♠️6": 6, "♠️7": 7, "♠️8": 8, "♠️9": 9, "♠️10": 10, "♠️11": 11, "♠️12": 12, "♠️13": 13,
          "♥️1": 1, "♥️2": 2, "♥️3": 3, "♥️4": 4, "♥️5": 5, "♥️6": 6, "♥️7": 7, "♥️8": 8, "♥️9": 9, "♥️10": 10, "♥️11": 11, "♥️12": 12, "♥️13": 13,
          "♦️1": 1, "♦️2": 2, "♦️3": 3, "♦️4": 4, "♦️5": 5, "♦️6": 6, "♦️7": 7, "♦️8": 8, "♦️9": 9, "♦️10": 10, "♦️11": 11, "♦️12": 12, "♦️13": 13,
          "♣️1": 1, "♣️2": 2, "♣️3": 3, "♣️4": 4, "♣️5": 5, "♣️6": 6, "♣️7": 7, "♣️8": 8, "♣️9": 9, "♣️10": 10, "♣️11": 11, "♣️12": 12, "♣️13": 13}


class Poker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = ["♠️1", "♠️2", "♠️3", "♠️4", "♠️5", "♠️6", "♠️7", "♠️8", "♠️9", "♠️10", "♠️11", "♠️12", "♠️13",
                      "♥️1", "♥️2", "♥️3", "♥️4", "♥️5", "♥️6", "♥️7", "♥️8", "♥️9", "♥️10", "♥️11", "♥️12", "♥️13",
                      "♦️1", "♦️2", "♦️3", "♦️4", "♦️5", "♦️6", "♦️7", "♦️8", "♦️9", "♦️10", "♦️11", "♦️12", "♦️13",
                      "♣️1", "♣️2", "♣️3", "♣️4", "♣️5", "♣️6", "♣️7", "♣️8", "♣️9", "♣️10", "♣️11", "♣️12", "♣️13"]  # array of deck of cards
        self.money = 0
        self.pot = 0
        self.round_num = 0
        self.game_start = False
        self.game_handler = None

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
        self.cards.remove(round_card)
        return round_card

    @commands.command()
    async def poker(self, ctx, **kwargs):
        # detect the command
        print(ctx.message.content)
        if 'start' in ctx.message.content:
            self.game_handler = 'start'
        elif 'bet' in ctx.message.content:
            self.game_handler = 'bet'
            bet_amount = int(ctx.message.content.split(' ')[2])
        elif 'fold' in ctx.message.content:
            self.game_handler = 'fold'
        if self.game_handler == "start":
            self.game_start = True
            self.pot = 0
            self.round_num = 1
            self.money = 2500
            # random card from deck
            # when we take a card from a deck, we are removing the card
            hand = self.deal()
            await ctx.send(hand[0])
            await ctx.send(hand[1])

        elif self.game_handler == "bet":
            if self.round_num == 1:
                card1 = self.round(int(bet_amount))
                await ctx.send(card1)
                self.round_num += 1
            elif self.round_num == 2:
                card2 = self.round(int(bet_amount))
                await ctx.send(card2)
                self.round_num += 1
            elif self.round_num == 3:
                card3 = self.round(int(bet_amount))
                await ctx.send(card3)
                self.round_num += 1

        elif self.game_handler == "fold":
            self.game_start == False


client.add_cog(Poker(client))


@client.command()
async def gamba(ctx, *, gambaamount=10):
    for messagecount in range(0, gambaamount):
        await ctx.send("GAMBA ")


client.run(
    token.read())
