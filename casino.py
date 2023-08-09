import discord
from discord.ext import commands
from economy import Economy, load, dump
from poker import Poker
from blackjack import Blackjack
from roulette import Roulette
import json

token = open('C:/Users/Luke/Documents/casino/token.txt')

client = commands.Bot(
    command_prefix='!', intents=discord.Intents.all(), )  # v2

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.add_cog(Economy(bot=client))
    await client.add_cog(Poker(bot=client))
    await client.add_cog(Blackjack(bot=client))
    await client.add_cog(Roulette(bot=client))



client.run(
    token.read())
