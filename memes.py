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
from React import win_slips
import io
import aiohttp
import scrape_google_images
import re

class CustomerHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{["!" + command.name + " " + command.help for command in mapping[cog]]}')

        
meme_list = pd.read_csv('Resources/meme_repository.csv')
react_list = pd.read_csv('Resources/react_repository.csv')
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
    all_quote_df = all_quote_df.drop((all_quote_df.columns[0]), axis=1).reset_index(drop=True)
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
    quote_df = quote_df.T
    quote_df.to_csv('fixer.csv')
    quote_df = pd.read_csv('fixer.csv')
    quote_df.columns = quote_df.iloc[0]
    quote_df = quote_df.drop(quote_df.index[0]).reset_index(drop=True)
    print(quote_df)
    all_quote_df= pd.concat([all_quote_df, quote_df], ignore_index=True)
    print(all_quote_df)
    all_quote_df.to_csv('Resources/quote_df.csv')

@bot.command(name='quote_this', help='This will add what you replied to as a quote')
async def quote_this(ctx):
    all_quote_df = pd.read_csv('Resources/quote_df.csv')
    all_quote_df = all_quote_df.drop((all_quote_df.columns[0]), axis=1).reset_index(drop=True)
    text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    name = text.author.name
    quote = text.content
    new_quote = {}
    new_quote['Name'] = 'Quote'
    new_quote[name] = quote
    quote_list = []
    quote_list.append(new_quote)
    await ctx.send(f"name is {name} and quote is {quote}")
    quote_df = pd.DataFrame.from_dict(quote_list)
    quote_df = quote_df.T
    quote_df.to_csv('fixer.csv')
    quote_df = pd.read_csv('fixer.csv')
    quote_df.columns = quote_df.iloc[0]
    quote_df = quote_df.drop(quote_df.index[0]).reset_index(drop=True)
    all_quote_df= pd.concat([all_quote_df, quote_df], ignore_index=True)
    all_quote_df.to_csv('Resources/quote_df.csv')


@bot.command(name='quote', help='This will call a random quote')
async def get_quote(ctx):
    quote_df = pd.read_csv('Resources/quote_df.csv')
    quote_row = quote_df.sample().reset_index(drop=True)
    name = quote_row['Name'][0]
    quote = quote_row['Quote'][0]
    await ctx.send(f'"{quote}"- {name}')
    quote_df.to_csv('fixer.csv')
    quote_df = pd.read_csv('fixer.csv')
    quote_df.columns = quote_df.iloc[0]
    quote_df = quote_df.drop(quote_df.index[0]).reset_index(drop=True)

@bot.command(name='quote_by', help='This will get a quote from a specific author')
async def get_quoteby(ctx, name):
    quote_df = pd.read_csv('Resources/quote_df.csv')
    filter = name
    filtered = quote_df.loc[quote_df['Name'].str.contains(filter)]
    filtered_row = filtered.sample().reset_index(drop=True)
    author = filtered_row['Name'][0]
    quote = filtered_row['Quote'][0]
    await ctx.send(f'"{quote}"-{author}')

@bot.command(name='quote_with', help='This will call a quote containing the word(s) invoked')
async def get_quotewith(ctx, fragment):
    quote_df = pd.read_csv('Resources/quote_df.csv')
    filter = fragment
    filtered = quote_df.loc[quote_df['Quote'].str.contains(filter)]
    filtered_row = filtered.sample().reset_index(drop=True)
    author = filtered_row['Name'][0]
    quote = filtered_row['Quote'][0]
    await ctx.send(f'"{quote}"-{author}')


@bot.command(name='self_burn', help='insult yourself')
async def get_burn(ctx):
    # Corey's User ID
    if ctx.message.author.id == 685569047739236408:
        await ctx.send('I cannot insult you, you are too perfect')
        sleep(10)
        await ctx.send("JK - Kingdom Hearts is a terrible franchise I can say that, I've been waiting for KH3 for 14 years")
    # Mickey's User ID
    elif ctx.message.author.id == 254099072695140352:
        await ctx.send('I cannot insult you, you are too perfect')
        sleep(10)
        await ctx.send('Futaba')
    else:
        await ctx.send('I cannot insult you, you are too perfect')

@bot.command(name='5050', help='It will either burn you or bless you luck of the draw and all that')
async def fifty(ctx):
    phrases = ['perfect', 'a true friend in these trying times', 'a gigachad', 'based asf', 'a man of culture',\
        'a gift', 'someone who I respect', 'my homie', 'a fellow warrior whom I treat with honor', 'a real gamer',\
            'kinda cringe tbh', 'not very cash money', 'a third rate duelist with a fourth rate deck', 'mids', 'a normie',\
                'a proud Anthem owner', 'a paste connoisseur', 'a Belieber', 'a narc', 'like that annoying npc from the starter town']
    name = ctx.message.author.name
    phrase = phrases[random.randint(0,(len(phrases) -1))]
    await ctx.send(f'{name} you are {phrase}')

@bot.command(name='win', help='shows you what happens when you are winning')
async def win(ctx):
    filepath = win_slips
    await ctx.send(file=discord.File(filepath))

@bot.command(name='react', help='tells you how to feel about something')
async def react(ctx):
    author = ctx.message.author.name
    single_react = react_list.sample().reset_index(drop=True)
    filepath = single_react['Filepath'].values[0]
    phrases = ['happy', 'sad', 'lazy', 'hopeless', 'miserable', 'full of ennui', 'despair', 'joy', 'ligma', 'testy', 'frustrated', 'horny', 'violent', 'mopey', 'sprightly']
    feeling = phrases[random.randint(0,(len(phrases)-1))]
    await ctx.send(f'{author} you should feel {feeling} clearly as shown here:', file=discord.File(filepath))

@bot.command(name='news', help='calls mufti news forth')
async def news(ctx):
    if ctx.message.reference is not None:
        text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        message = text.content
        await text.reply(f'{name} that is haram')


# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     # Corey's User ID
#     if message.author.id == 685569047739236408 and not message.content.startswith("Oh beautiful bot"):
#         await message.channel.send('meep')
#     check = message.content.lower()
#     regex = r"\bign|ign.com"
#     if re.search(regex, check):
#         if message.reference is None:
#             async with aiohttp.ClientSession() as session:
#                 link = scrape_google_images.get_random_image_link_from_google('ign memes')
#                 async with session.get(link) as resp:
#                     if resp.status != 200:
#                         return await message.channel.send('Damn it Corey, you broke it')
#                     data = io.BytesIO(await resp.read())
#                     await message.channel.send(file=discord.File(data, link))
#     await bot.process_commands(message)



bot.run(token)

