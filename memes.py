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

        
chug_counter = 0
meme_list = pd.read_csv('Resources/meme_repository.csv')
react_list = pd.read_csv('Resources/react_repository.csv')
load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents(messages=True, message_content=True, guilds=True, members=True), help_command=CustomerHelpCommand())
client = discord.Client(intents=discord.Intents(messages=True, message_content=True, guilds=True, members=True))
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


@bot.command(name='train', help='chugga chugga')
async def train(ctx):
    global chug_counter
    chugga = [' chugga ', 'chugga ', 'chOO ', 'CHOO ']
    return_val = "Look out the train's a coming"
    if chug_counter < 4:
        range_lim = chug_counter + 1
        for i in range(0, range_lim):
            chug = chugga[i]
            return_val = return_val + chug
        await ctx.send(return_val)
        chug_counter += 1
    elif chug_counter >= 4:
        return_val = "Whew that was close the train just left"
        chug_counter = 0
        await ctx.send(return_val)

@bot.command(name='whats_this', help='fixes incorrect speech')
async def uwu(ctx):
    if ctx.message.reference is not None:
        text = await ctx.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        message = text.content
        fixes = ['l', 'r', 'L', 'R']
        for val in fixes:
            message = message.replace(val, 'w')
        await text.reply(f'uwu {name} I think you mean {message}')

@bot.command(name='dilemma', help='This calls up a moral dilemma of unfathomable difficulty')
async def trolley(ctx):
    if ctx.message.author.bot:
        return
    members = ctx.guild.members
    user_list = []
    modifier_list = ['Clifford the Big Red Dog', 'Charlie Sheen', 'a real wizard', 'the potion seller', 'a sad looking horse', 'the ghost of my hopes and dreams', 'a cute puppy',\
        'terminally sick orphans', 'Naruto Uzamaki', 'a real life catgirl', 'the inventor of femboy hooters', 'Jeff Bezos', "Tupac (he's always been alive idiot)", 'Aslan',\
            'Rick Astley', 'Ligma Larry', 'Steve Jobs', 'an Italian chef', 'the guy who decided to put all that sugar into PF Changs sauce']
    for member in members:
       user_list.append(member.name)
    user_list.remove(ctx.message.author.name)
    first_track_name = user_list[random.randint(0,(len(user_list) - 1))]
    user_list.remove(first_track_name)
    second_track_name = user_list[random.randint(0,(len(user_list) - 1))]
    first_track_modifier = modifier_list[random.randint(0,(len(modifier_list) - 1))]
    modifier_list.remove(first_track_modifier)
    second_track_modifier = modifier_list[random.randint(0,(len(modifier_list) - 1))]
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    await ctx.send(f'You are sitting at the switch for trolley tracks to your left you see {first_track_name} and {first_track_modifier} tied to the track, on the right track you see {second_track_name} and {second_track_modifier} tied down a trolley is hurtling towards you and these individuals who do you save the left or right track?')
    side_msg = await bot.wait_for('message', check=check)
    side = side_msg.content
    side = side.lower()
    await ctx.send(f'You said {side}')
    if side == 'left':
        await ctx.send(f'You chose to let {second_track_name} and {second_track_modifier} die. Congratulations!')
    if side == 'right':
        await ctx.send(f'You chose to let {first_track_name} and {first_track_modifier} die. Congraulations!')

@bot.command(name='14', help='This correct names FFXIV')
async def ffxiv(ctx):
    if ctx.message.author.bot:
        return
    if ctx.message.reference is not None:
        text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        pasta = 'The critically acclaimed MMORPG Final Fantasy XIV? With an expanded free trial which you can play through the entirety of A Realm Reborn and the award winning Heavensward expansion up to level 60 for free with no restrictions on playtime'    
        await ctx.send(f'{name} are you referring to {pasta}?')
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

