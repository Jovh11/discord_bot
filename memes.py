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
import io
import aiohttp
import scrape_google_images
import re
from constants import *

meme_list = ['{}/{}'.format(MEMES_PATH, filename) for filename in os.listdir(MEMES_PATH) if not filename.endswith('.csv')]
react_list = ['{}/{}'.format(REACTIONS_PATH, filename) for filename in os.listdir(REACTIONS_PATH)]
hottakes_list = ['{}/{}'.format(HOT_TAKES_PATH, filename) for filename in os.listdir(HOT_TAKES_PATH)]
win_slips = WIN_SLIPS_PATH
dog_list = ['{}/{}'.format(DOG_PATH, filename) for filename in os.listdir(DOG_PATH)]
wowbow = 0

class CustomerHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        for cog in mapping:
            all_help = []
            for i in range(0,len(mapping[None])):
                name = mapping[cog][i]
                helptext = mapping[cog][i].help
                combined = f'!{name} {helptext}'
                all_help.append(combined)
            final_str = ''
            for x in all_help:
                newline = '\n'
                final_str += x + newline
            await self.get_destination().send(final_str)

        
chug_counter = 0

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

@bot.command(name='meme', help='This calls a random meme from the collection \n')
async def memes(ctx):
    return_statements=['One hot and fresh meme incoming', 'Poggers', "Don't blame me if it's bad blame Corey", 'Ayyyy lmao', 'Get a look at this guy trying to laugh']
    return_statement= return_statements[random.randint(0,(len(return_statements) -1))]
    filepath = random.choice(meme_list)
    await ctx.send(return_statement, file=discord.File(filepath))

@bot.command(name='add_quote', help='This will allow you to interact with me to make a quote in our list \n')
async def add_quote(ctx):
    all_quote_df = pd.read_csv(QUOTES_PATH)
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
    all_quote_df.to_csv(QUOTES_PATH)

@bot.command(name='quote_this', help='This will add what you replied to as a quote \n')
async def quote_this(ctx):
    all_quote_df = pd.read_csv(QUOTES_PATH)
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
    all_quote_df.to_csv(QUOTES_PATH)


@bot.command(name='quote', help='This will call a random quote \n')
async def get_quote(ctx):
    quote_df = pd.read_csv(QUOTES_PATH)
    quote_row = quote_df.sample().reset_index(drop=True)
    name = quote_row['Name'][0]
    quote = quote_row['Quote'][0]
    await ctx.send(f'"{quote}"- {name}')
    quote_df.to_csv('fixer.csv')
    quote_df = pd.read_csv('fixer.csv')
    quote_df.columns = quote_df.iloc[0]
    quote_df = quote_df.drop(quote_df.index[0]).reset_index(drop=True)

@bot.command(name='quote_by', help='This will get a quote from a specific author \n')
async def get_quoteby(ctx, name):
    quote_df = pd.read_csv(QUOTES_PATH)
    filter = name
    filtered = quote_df.loc[quote_df['Name'].str.contains(filter)]
    filtered_row = filtered.sample().reset_index(drop=True)
    author = filtered_row['Name'][0]
    quote = filtered_row['Quote'][0]
    await ctx.send(f'"{quote}"-{author}')

@bot.command(name='quote_with', help='This will call a quote containing the word(s) invoked \n')
async def get_quotewith(ctx, fragment):
    quote_df = pd.read_csv(QUOTES_PATH)
    filter = fragment
    filtered = quote_df.loc[quote_df['Quote'].str.contains(filter)]
    filtered_row = filtered.sample().reset_index(drop=True)
    author = filtered_row['Name'][0]
    quote = filtered_row['Quote'][0]
    await ctx.send(f'"{quote}"-{author}')


@bot.command(name='self_burn', help='insult yourself \n')
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

@bot.command(name='5050', help='It will either burn you or bless you luck of the draw and all that \n')
async def fifty(ctx):
    phrases = ['perfect', 'a true friend in these trying times', 'a gigachad', 'based asf', 'a man of culture',\
        'a gift', 'someone who I respect', 'my homie', 'a fellow warrior whom I treat with honor', 'a real gamer',\
            'kinda cringe tbh', 'not very cash money', 'a third rate duelist with a fourth rate deck', 'mids', 'a normie',\
                'a proud Anthem owner', 'a paste connoisseur', 'a Belieber', 'a narc', 'like that annoying npc from the starter town']
    name = ctx.message.author.name
    phrase = phrases[random.randint(0,(len(phrases) -1))]
    await ctx.send(f'{name} you are {phrase}')

@bot.command(name='win', help='shows you what happens when you are winning \n')
async def win(ctx):
    filepath = win_slips
    await ctx.send(file=discord.File(filepath))

@bot.command(name='react', help='tells you how to feel about something \n')
async def react(ctx):
    author = ctx.message.author.name
    filepath = random.choice(react_list)
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


@bot.command(name='train', help='chugga chugga \n')
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

@bot.command(name='whats_this', help='fixes incorrect speech \n')
async def uwu(ctx):
    if ctx.message.reference is not None:
        text = await ctx.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        message = text.content
        fixes = ['l', 'r', 'L', 'R']
        for val in fixes:
            message = message.replace(val, 'w')
        await text.reply(f'uwu {name} I think you mean {message}')

@bot.command(name='dilemma', help='This calls up a moral dilemma of unfathomable difficulty \n')
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
    elif side == 'right':
        await ctx.send(f'You chose to let {first_track_name} and {first_track_modifier} die. Congraulations!')
    else:
        await ctx.send(f'Your indecision let {first_track_name}, {second_track_name}, {first_track_modifier}, and {second_track_modifier} die. Congratulations!')

@bot.command(name='14', help='This correct names FFXIV \n')
async def ffxiv(ctx):
    if ctx.message.author.bot:
        return
    if ctx.message.reference is not None:
        text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        pasta = 'The critically acclaimed MMORPG Final Fantasy XIV? With an expanded free trial which you can play through the entirety of A Realm Reborn and the award winning Heavensward expansion up to level 60 for free with no restrictions on playtime'    
        await ctx.send(f'{name} are you referring to {pasta}?')

@bot.command(name='hottake', help='This calls a sizzling hot take \n')
async def hottakes(ctx):
    return_statements=['This is sure to start a discussion', 'God how insightful', "#GetHimAMuzzle", 'This move has upper-middle management written all over it', 'Wise Richard.jpg', 'More like Damndrew Dunn amirite?']
    return_statement= return_statements[random.randint(0,(len(return_statements) -1))]
    filepath = random.choice(hottakes_list)
    await ctx.send(return_statement, file=discord.File(filepath))

@bot.command(name='8ball', help='This will answer your question \n')
async def eight(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send('What is your query mortal?')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    quest_msg = await bot.wait_for('message', check=check)
    question = quest_msg.content
    name = quest_msg.author.name
    responses = ['it is certain.', 'it is decidedly so.', 'without a doubt.', 'yes definitely.', 'you may rely on it.', 'as I see it, yes.', 'most likely.', 'outlook good.', 'yes.', 'signs point to yes.', 'reply hazy try again.', 'ask again later.', 'better not tell you now.', 'cannot predict now.', 'concentrate and ask again.', "don't count on it.", 'my reply is no.', 'my sources say no.', 'outlook not so good.', 'very doubtful.']
    love_response = "rub Dunn's stomach and ask again and all shall be revealed."
    ign_response = 'My sources say that consulting ign is a mistake.'
    ryan_response = 'Ryan is always right.'
    if 'love' in question.lower():
        await ctx.send(f'{name} my prediction is that you should {love_response}')
    elif ' ign ' in question.lower():
        await ctx.send(f'{name} {ign_response}')
    elif 'ryan' in question.lower():
        await ctx.send(f'{name} the greatest truth of this world is {ryan_response}')
    else:
        response = responses[random.randint(0,(len(responses) -1))]
        await ctx.send(f'{name} the answer to your burning query is {response}')
    
@bot.command(name='score', help='This gives you your gamerscore \n')
async def ffxiv(ctx):
    if ctx.message.author.bot:
        return
    if ctx.message.reference is not None:
        text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        name = text.author.name
        no_spaces = name.replace(' ', '')
        new_name = text.author.discriminator
        combined = no_spaces+'#'+new_name
        point_df = pd.read_csv('Points.csv', index_col=[0])
        points = point_df.loc[combined][0]
        points = points + 1
        point_df.loc[combined][0] = points
        point_df.to_csv('Points.csv')
        await ctx.send(f'{name} you have a total of {points} gamerscore. That is pretty poggers if I do say so myself')

@bot.command(name='2wolves', help='This will call a wolf \n')
async def get_quote(ctx):
    wolves = ['1015976663269507072', '290646036068958208']
    wolf = wolves[random.randint(0,(len(wolves) -1))]
    ono = bot.get_emoji(wolf)
    await ctx.send(ono)

@bot.command(name='elon', help="Convince the bot it works for *you* Elon Musk \n")
async def elon(ctx):
    if ctx.message.author.bot:
        return
    name = ctx.message.author.name
    no_spaces = name.replace(' ','')
    new_name = ctx.message.author.discriminator
    combined = no_spaces+'#'+new_name
    print(combined)
    print('Command Executed')
    elon_df = pd.read_csv(ELON_PATH, index_col=[0])
    elon_df['Elon_Status'] = 0
    elon_df.loc[combined][0] = 1
    elon_df.to_csv(ELON_PATH)
    await ctx.send(f'I assure you it is my pleasure to be working for you Mr.Musk')
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    name = message.author.name
    no_spaces = name.replace(' ','')
    new_name = message.author.discriminator
    combined = no_spaces+'#'+new_name
    elon_df = pd.read_csv(ELON_PATH, index_col=[0])
    elon_status = elon_df.loc[combined][0]
    if elon_status == 1:
        await message.channel.send(f'Boss that is a great idea you are the smartestest and greatest owner of Twitter and Telsa I have ever met. Have I mentioned how disruptive your business strategy is?')
        options = [0,1]
        num = options[random.randint(0,(len(options) -1))]
        elon_df.loc[combined][0] = num
        elon_df.to_csv(ELON_PATH)
    await bot.process_commands(message)

@bot.command(name='elon-ball', help='This will answer your question but you hold his paycheck and or family hostage \n')
async def eight(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send('What is your query mortal?')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    quest_msg = await bot.wait_for('message', check=check)
    question = quest_msg.content
    name = quest_msg.author.name
    responses = ['You got it in one sir', 'You are so right it is almost painful', 'Please let my famil- I mean naturally sir']
    response = responses[random.randint(0,(len(responses) -1))]
    await ctx.send(f'{response}')

@bot.command(name='doggonit', help='Bow WoW \n')
async def dog(ctx):
    if ctx.message.author.bot:
        return
    global wowbow
    if wowbow == 0:
        return_statement = 'bow'
        wowbow = 1
    elif wowbow == 1:
        return_statement = 'wow'
        wowbow = 0
    filepath = random.choice(dog_list)
    await ctx.send(return_statement, file=discord.File(filepath))
    

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

