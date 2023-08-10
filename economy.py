import json
from discord.ext import commands
import discord

def dump(user_money):
    with open('bank.txt', 'w') as file:
        file.write(json.dumps(user_money))

def load():
    with open('bank.txt', 'r') as file:
        return json.loads(file.read())

user_money = load()

def add(user, amount, user_money):
    user_money[str(user.id)] += amount
    dump(user_money)

def subtract(user, amount, user_money):
    user_money[str(user.id)] -= amount
    dump(user_money)

def change(user, amount, user_money):
    user_money[str(user.id)] = amount
    dump(user_money)
        
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx, user: discord.Member = None):
        # Check if the user has a balance in the dictionary
        if not user:  # checks if there was a user in command
            user = ctx.author 
        if str(user.id) in user_money:  # checks if user is in dictionary
            await ctx.send(f"{user.mention}'s current balance is ${user_money[str(user.id)]:,.2f}")
        else:
            # otherwise give a balance to user
            change(user, 2500, user_money)
            await ctx.send(f"{user.mention}'s current balance is ${user_money[str(user.id)]:,.2f}")


    @commands.command()
    async def give(self, ctx, user: discord.Member, amount: float):
        # Check if the sender has enough money to give
        if str(ctx.author.id) not in user_money or user_money[str(ctx.author.id)] < amount:
            await ctx.send('You do not have enough money to give.')
            return

        # Subtract the given amount from the sender's balance and add it to the recipient's balance
        subtract(ctx.author, amount, user_money)
        if str(user.id) in user_money:
            add(user, amount, user)
        else:
            change(user, amount + 2500, user_money)
        await ctx.send(f'{ctx.author.mention} gave {user.mention} ${amount:,.2f}')
        
    