from imaplib import Commands
from time import sleep
import pandas as pd
import numpy as np
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import token, server
import asyncio
import random

class CustomerHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{["!" + command.name + " " + command.help for command in mapping[cog]]}')

        
meme_list = pd.read_csv('Resources/meme_repository.csv')
load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents(messages=True, message_content=True), help_command=CustomerHelpCommand())
client = discord.Client(intents=discord.Intents(messages=True, message_content=True))
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == server:
            break
    
    print(f'{client.user} has connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})'
        )

@bot.command(name='meme', help='This calls a random meme from the collection')
async def memes(ctx):
    return_statements=['One hot and fresh meme incoming', 'Poggers', "Don't blame me if it's bad blame Corey", 'Ayyyy lmao', 'Get a look at this guy trying to laugh']
    return_statement= return_statements[random.randint(0,(len(return_statements) -1))]
    single_meme = meme_list.sample().reset_index(drop=True)
    filepath = single_meme['Filepath'].values[0]
    await ctx.send(return_statement, file=discord.File(filepath))

@bot.command(name='add_quote', help='This will allow you to interact with me to make a quote in our list')
async def add_quote(ctx):
    all_quote_df = pd.read_csv('Resources/quote_df.csv')
    #all_quote_df.columns = all_quote_df.iloc[0]
    #all_quote_df = all_quote_df.drop(all_quote_df.index[0]).reset_index(drop=True)
    all_quote_df = all_quote_df.drop((all_quote_df.columns[0]), axis=1).reset_index(drop=True)
    print(all_quote_df)
    i = 0
    await ctx.send('Who said the quote?')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    new_quote = {}
    while i < 1:
        name_msg = await bot.wait_for('message', check=check)
        name = name_msg.content
        await ctx.send(f'You said {name}')
        i+=1
    await ctx.send("What is the quote?")
    while i < 2:
        quote_msg = await bot.wait_for('message', check=check)
        quote = quote_msg.content
        i += 1
    new_quote['Name'] = 'Quote'
    new_quote[name] = quote
    quote_list = []
    quote_list.append(new_quote)
    await ctx.send(f"name is {name} and quote is {quote}")
    quote_df = pd.DataFrame.from_dict(quote_list)
    #print(quote_df)
    #quote_df = quote_df.rename(columns={0:'Name', 1:'Quote'})
    quote_df = quote_df.T
    #print(quote_df)
    quote_df.to_csv('fixer.csv')
    quote_df = pd.read_csv('fixer.csv')
    quote_df.columns = quote_df.iloc[0]
    quote_df = quote_df.drop(quote_df.index[0]).reset_index(drop=True)
    #quote_df.to_csv('Resources/debug.csv')
    print(quote_df)
    all_quote_df= pd.concat([all_quote_df, quote_df], ignore_index=True)
    print(all_quote_df)
    all_quote_df.to_csv('Resources/quote_df.csv')

@bot.command(name='quote', help='This will call a random quote')
async def get_quote(ctx):
    quote_df = pd.read_csv('Resources/quote_df.csv')
    quote_row = quote_df.sample().reset_index(drop=True)
    print(quote_df)
    print(quote_row)
    name = quote_row['Name'][0]
    quote = quote_row['Quote'][0]
    await ctx.send(f'"{quote}"- {name}')

@bot.command(name='self_burn', help='insult yourself')
async def get_burn(ctx):
    # Corey's User ID
    if ctx.message.author.id == 685569047739236408:
        await ctx.send('I cannot insult you, you are too perfect')
        sleep(10)
        await ctx.send("JK - Kingdom Hearts is a terrible franchise I can say that, I've been waiting for KH3 for 14 years")
    # Mickey's User ID
    elif ctx.message.author.id == 254099072695140352:
        await ctx.send('Futaba')
    else:
        await ctx.send('I cannot insult you, you are too perfect')

bot.run(token)

