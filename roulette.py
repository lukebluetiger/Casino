import discord
from discord.ext import commands
import random
from economy import load, dump

user_money = load()

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bets = {}  
        self.money = 0
        self.pot = 0
        self.game_start = False

    @commands.command()
    async def roulette(self, ctx, *, bet):
        wheel = {0:'green',1:'red',2:'black',3:'red',4:'black',5:'red',6:'black',7:'red',8:'black',9:'red',10:'black',11:'black',12:'red',13:'black',14:'red',15:'black',16:'red',17:'black',18:'red'
                ,19:'black',20:'black',21:'red',22:'black',23:'red',24:'black',25:'red',26:'black',27:'red',28:'black', 29:'black',30:'red',31:'black',32:'red',33:'black',34:'red',35:'black',36:'red'}
        
        if self.game_start == False:
            if bet == "start":
                self.bets = {}
                if ctx.author.id not in user_money:  # from our 'balance' command
                        user_money[ctx.author.id] = 2500.00
                self.money = user_money[ctx.author.id]
                await ctx.send(f"Spinning. Use `!roulette <bet> <amount>`, or use `!roulette stop` to end!")
                self.game_start = True
        
        elif self.game_start == True:
            x = bet.split(" ") # split message by space 
            if len(x) == 2:
                bet_amount = int(x[1]) # amount is second argument
            bet = str(x[0]) # bet is first
            if bet == "stop":
                result = [] 
                result.append(random.randint(0, 35))
                result.append(wheel[result[0]]) # append both results (number and color)
                await ctx.send("Betting over! Result of spin: `{} {}`.".format(result[1], result[0]))
                if result[0] in self.bets.keys(): # if the number is correct that means the player wins more
                    self.money += (35 * self.bets[result[0]])
                    user_money[ctx.author.id] = self.money
                    await ctx.send("Won `${}`. Current balance is `${}`".format(35 * self.bets[result[0]], self.money))
                elif result[1] in self.bets.keys():
                    self.money += (2 * self.bets[result[1]])
                    user_money[ctx.author.id] = self.money
                    await ctx.send("Won `${}`. Current balance is `${}`".format(2 * self.bets[result[1]], self.money))
            if bet in wheel.values():
                self.bets[bet] = bet_amount
                self.money -= bet_amount
                user_money[ctx.author.id] = self.money
                await ctx.send("`${}` on `{}`.".format(self.bets[bet], bet))
            try: # catch the exception so the player wont get an error for not betting on a number
                if int(bet) in wheel.keys():
                    self.bets[int(bet)] = bet_amount
                    self.money -= bet_amount
                    user_money[ctx.author.id] = self.money
                    await ctx.send("`${}` on `{}`.".format(self.bets[int(bet)], int(bet)))
            except:
                return
        