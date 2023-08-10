import discord
from discord.ext import commands
import random
from economy import load, change

user_money = load()

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
        change(ctx.author, self.money, user_money)

    @commands.command(name='blackjack')
    async def blackjack(self, ctx, *, game_handler):
        # commands that can be used outside a game
        if game_handler == "help":
            return await ctx.send("`\n start (amount) - starts the game with bet amount \n hit - retrieves a new card from the deck \n fold - folds the for the current game \n rules - displays the rules for the game`")

        if game_handler == "rules":
            return await ctx.send("`\n This version of Blackjack is played against the bot. Players bet in round one with !blackjack start (bet). The player then hits until they're as close to 21 as possible, and then they use stand to reveal the opponents cards. The Dealer must hit until above 17, and then the winner recieves a return of 1.5 * their bet.`")
        elif not self.game_start: # to confirm there is not a game currently happening 
            if "start" in game_handler:
                self.game_start = True
                try:  # for a default bet
                    bet_amount = int(game_handler.lstrip("start "))
                except:
                    bet_amount = 100.00
                if str(ctx.author.id) not in user_money:  # from our 'balance' command
                     change(ctx.author, 2500, user_money)
                self.money = user_money[str(ctx.author.id)]
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
                change(ctx.author, self.money, user_money)
                await ctx.send(f"${bet_amount:,.2f} add to the pot.")
                await ctx.send("Dealer: ` ` `{}`".format(self.bot_hand[1]))
                await ctx.send("Hand: `{}` `{}`. What would you like to do?".format(self.hand[0], self.hand[1]))
            else:
                await ctx.send("You must be in a game to use this command! Use `!blackjack start` to start!") # else the player is probably trying to use a game specific command while not in a game   
        
        elif self.game_start:
            if game_handler == "hit":
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
                change(ctx.author, self.money, user_money)
                self.game_start = False
