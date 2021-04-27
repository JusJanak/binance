import binance
import discord
import json

from config import config
from binance.client import Client
from discord.ext import commands

client = Client(config['api_key'], config['api_secret'])
bot = commands.Bot(command_prefix = config['prefix'])


async def generate_data(crpyto_name: str):
    return client.get_symbol_info(crpyto_name)

@bot.event
async def on_ready():
    print('Bot is ready...')


@bot.event
async def on_message(msg):
    if not msg.content.startswith(config['prefix']):
        return

    crypto_name = None
    data = None

    try:
        if msg.content.lower().startswith(config['prefix'] + 'bnb'):
            crypto_name = msg.content.upper().split(config['prefix'])[1]
        else:
            crypto_name = 'BNB' + msg.content.upper().split(config['prefix'])[1]

        data = await generate_data(crypto_name)
    except:
        await msg.channel.send('Are you sure that ' + msg.content.split(config['prefix'])[1] + ' is a real crypto-currency?')
    
    if not data:
        print(1)
        return
    else:
        print(data)

    embed = discord.Embed(
        title = crypto_name, 
        color = 0xFFD700
    )

    await bot.process_commands(msg)


#@bot.command(name = "ServerStatus", aliases = ["serverstatus", "Serverstatus", "serverStatus"])
#async def status_command(ctx):



bot.run(config['bot_token'])