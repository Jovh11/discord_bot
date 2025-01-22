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
# from constants import *

MEMES_PATH = "X:\Pictures\Memes"
REACTIONS_PATH = "X:\Pictures\Reactions"
HOT_TAKES_PATH = "X:\Pictures\Recipts\All"
WIN_SLIPS_PATH = "X:\Pictures\Reactions\win.jpg"
DOG_PATH = "X:\Pictures\Dogs"
QUOTES_PATH = r"C:\Users\rcrch\Documents\Git\discord_bot\quote_df.csv"
SERVER_TOPICS_PATH = r"C:\Users\rcrch\Documents\Git\discord_bot\Resources\server.csv"
# cat_path = ""
meme_list = ['{}/{}'.format(MEMES_PATH, filename) for filename in os.listdir(MEMES_PATH) if not filename.endswith('.csv')]
react_list = ['{}/{}'.format(REACTIONS_PATH, filename) for filename in os.listdir(REACTIONS_PATH)]
hottakes_list = ['{}/{}'.format(HOT_TAKES_PATH, filename) for filename in os.listdir(HOT_TAKES_PATH)]
win_slips = WIN_SLIPS_PATH
dog_list = ['{}/{}'.format(DOG_PATH, filename) for filename in os.listdir(DOG_PATH)]
# cat_list = ['{}/{}'.format(CAT_PATH, filename) for filename in os.listdir(DOG_PATH) if not filename.endswith('.csv')]
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
    meme_list = ['{}/{}'.format(MEMES_PATH, filename) for filename in os.listdir(MEMES_PATH) if not filename.endswith('.csv')]
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
        if '@' in name and '@ ' not in name:
            name = name.replace('@','@ ')
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
    hottakes_list = ['{}/{}'.format(HOT_TAKES_PATH, filename) for filename in os.listdir(HOT_TAKES_PATH)]
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
    
# @bot.command(name='give_score', help='This gives you your friend a gamerscore \n')
# async def score_give(ctx):
#     if ctx.message.author.bot:
#         return
#     reply_message_id = ctx.message.reference.message_id
#     reply_message = await ctx.fetch_message(reply_message_id)
#     reply_author = reply_message.author
#     if reply_author == ctx.message.author:
#         await ctx.send("Sorry you can't give yourself points")
#     if ctx.message.reference is not None and reply_author != ctx.message.author:
#         text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#         name = text.author.name
#         name_id = text.author.id
#         point_df = pd.read_csv('Points.csv', index_col=[0])
#         points = point_df.loc[name_id]['Points']
#         points = int(points) + 1
#         point_df.at[name_id, "Points"] = points
#         point_df.to_csv('Points.csv')
#         await ctx.send(f"{name} you have {points} point(s). That is pretty poggers if I do say so myself.")

@bot.command(name="score_count", help="This will give you your gamerscore \n")
async def score_count(ctx):
    if ctx.message.author.bot:
        return
    name = ctx.message.author.name
    author = ctx.message.author.id
    point_df = pd.read_csv("Points.csv", index_col=[0])
    points  = point_df.loc[author]["Points"]
    await ctx.send(f"{name} you have {points} point(s) may it be a light in dark times")


@bot.command(name='2wolves', help='This will call a wolf \n')
async def get_quote(ctx):
    wolves = ['<:icelandicdunn:1007270960136728627>', '<:wiserichard:1007266810481090671>']
    wolf = wolves[random.randint(0,(len(wolves) -1))]
    await ctx.send(wolf)

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
    
    ## TODO: Fix Elon Command Username storage to be dynamic & remove try/except
    try:
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
    except:
        pass
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
    dog_list = ['{}/{}'.format(DOG_PATH, filename) for filename in os.listdir(DOG_PATH)]
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
    
@bot.command(name='catgonit', help='Caturday Came Early \n')
async def cat(ctx):
    cat_list = ['{}/{}'.format(CAT_PATH, filename) for filename in os.listdir(CAT_PATH) if not filename.endswith('.csv')]
    if ctx.message.author.bot:
        return
    ctx.send("Behold a feline")
    filepath = random.choice(cat_list)
    await ctx.send(file=discord.File(filepath))


@bot.command(name="add_dog", help='Insert a Doggo Picture \n')
async def woofer(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send('Please reply with a dog picture(s)')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel    
    image_msg = await bot.wait_for('message', check=check)
    image = image_msg.attachments
    for attachment in image:
        if valid_image_url(attachment.url):
            await attachment.save(os.path.join(f"{DOG_PATH}", attachment.filename))
    await ctx.send('Added Friend')

@bot.command(name="add_meme", help="Add a Meme \n")
async def memeadd(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send('Please reply with a meme if you trying to challenge my supremacy lesser memelord')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel    
    image_msg = await bot.wait_for('message', check=check)
    image = image_msg.attachments
    for attachment in image:
        if valid_image_url(attachment.url):
            await attachment.save(os.path.join(f"{MEMES_PATH}", attachment.filename))
    await ctx.send('Added coward')

@bot.command(name="add_cat", help="Add a cat picture \n")
async def catadd(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send('Please reply with a lesser beast')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel    
    image_msg = await bot.wait_for('message', check=check)
    image = image_msg.attachments
    for attachment in image:
        if valid_image_url(attachment.url):
            await attachment.save(os.path.join(f"{CAT_PATH}", attachment.filename))
    await ctx.send('Added cat lover')

def valid_image_url(url: str):
    image_extensions = ['png', 'jpg', 'jpeg', 'gif']
    for image_extension in image_extensions:
        if url.endswith('.' + image_extension):
            return True
    return False

@bot.command(name="add_take", help="Showcase that homegrown spice")
async def takeadd(ctx):
    if ctx.message.author.bot:
        return
    await ctx.send("Please reply with a spicy take")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    image_msg = await bot.wait_for('message', check=check)
    image = image_msg.attachments
    for attachment in image:
        if valid_image_url(attachment.url):
            await attachment.save(os.path.join(f"{HOT_TAKES_PATH}", attachment.filename))
    await ctx.send("Added the heat about dat boy")

@bot.command(name="topic", help="Help move the conversation along")
async def topic(ctx):
    food = ["Pancakes", "Waffles", "French Toast", "Pineapple Pizza", "Fruit (unripened)", "Fruit (ripened)", "Brussel Sprouts", "Vegemite Sandwich (Man from Brussels edition)", 
            "Apple Pie", "Pears", "Saltines", "Rice"]
    
    games = ["God of War Ragnarok", "God of War", "Elden Ring", "Sid Meier's Civilization V", "Age of Wonders 4", "Warhammer 40000: Darktide", "Fortnite", "Apex Legends",
             "Critically Acclaimed MMORPG Final Fantasy XIV Now Free Through Heavensword", "Allods", "Diablo IV", "Checkers"]
    
    shows = ["Game of Thrones", "One Piece", "Naruto Shippuden", "Chairham Anime", "Quints", "Gundam: Iron Blooded Orphans", "Gundam: The Witch from Mercury", "Mushoku Tensei",
             "The Office", "Parks and Recreation", "Ridiculousness", "The Jeselnik Offensive", "Late Night with Jimmy Fallon", "Family Feud", "The Price is Right"]
    
    miscellany = ["Magic: The Gathering", "Snorehammer 40K", "Cats", "Dogs", "Specifically Pepsi products", "The Big Bang Theory Laughtrack", "Formula One Racing",
                  "Bad TV", "Good Books", "Dune", "Avenging their clan"]
    
    def apples_to_apples(lst, name):
        size = len(lst)
        loc = random.randint(0, size -1)
        loc2 = random.randint(0, size -1)
        if loc == loc2:
            loc2 = random.randint(0, size -1)
        else:
            output_str = f"My powerful wizard orb has determined that {lst[loc]} is better than {lst[loc2]}. {name.mention} what do you think?"
        return output_str

    def apples_to_oranges(lst, lst2, name):
        size1 = len(lst)
        size2 = len(lst2)
        loc = random.randint(0, size1 -1)
        loc2 = random.randint(0, size2 -1)
        modifier = ["hate", "secretly love", "pretend to like", "love almost romantically", "want to lick", "never stop talking about"]
        loc3 = random.randint(0, len(modifier) -1)
        output_str = f"My secret scrying techniques (patent pending) has shown me that people who like {lst[loc]} often {modifier[loc3]} {lst2[loc2]} what do you think {name.mention}?"
        return output_str
    
    def get_id():
        df = pd.read_csv("Topic.csv")
        user_list = df['id'].values
        user_id = user_list[random.randint(0,(len(user_list) - 1))]
        return user_id

    topics = [food, games, shows, miscellany]
    prompt = random.randint(0,1)
    id = get_id()
    name = await bot.fetch_user(id)
    if prompt == 0:
        topicnum = random.randint(0, len(topics) -1)
        topic = topics[topicnum]
        output = apples_to_apples(topic, name)
        await ctx.send(output)
    elif prompt == 1:
        topicnum1 = random.randint(0, len(topics) -1)
        topicnum2 = random.randint(0, len(topics) -1)
        if topicnum1 == topicnum2:
            topicnum2 = random.randint(0, len(topics) -1)
        topic = topics[topicnum1]
        topic2 = topics[topicnum2]
        output = apples_to_oranges(topic, topic2, name)
        await ctx.send(output)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji.id == 1007263173361012927:
        value = reaction.emoji.id
        person = user.id
        message_id = reaction.message.id
        df = pd.read_csv("Reaction_Tracker.csv", index_col=[0])
        refined_df = df[df['Message id'] == message_id]
        users = refined_df['User id'].values
        more_refined_df = refined_df[refined_df['User id'] == person]
        emojis = more_refined_df['Reaction'].values
        if person not in users:
            together = {}
            together['Message id'] = [message_id]
            together['User id'] = [person]
            together['Reaction'] = [value]
            df2 = pd.DataFrame(together)
            df = pd.concat([df,df2])
            df.to_csv("Reaction_Tracker.csv")
            point_df = pd.read_csv('Points.csv', index_col=[0])
            point_reciever = reaction.message.author.id
            points = point_df.loc[point_reciever]['Points']
            points = int(points) + 1
            point_df.at[person, "Points"] = points
            point_df.to_csv('Points.csv')
        elif 1007263173361012927 not in emojis:
            together = {}
            together['Message id'] = [message_id]
            together['User id'] = [person]
            together['Reaction'] = [value]
            df2 = pd.DataFrame(together)
            df = pd.concat([df,df2])
            df.to_csv("Reaction_Tracker.csv")
            point_df = pd.read_csv('Points.csv', index_col=[0])
            point_reciever = reaction.message.author.id
            points = point_df.loc[point_reciever]['Points']
            points = int(points) + 1
            point_df.at[person, "Points"] = points
            point_df.to_csv('Points.csv')   
    elif reaction.emoji.id == 1007263123205533756:
        value = reaction.emoji.id
        person = user.id
        message_id = reaction.message.id
        df = pd.read_csv("Reaction_Tracker.csv", index_col=[0])
        refined_df = df[df['Message id'] == message_id]
        users = refined_df['User id'].values
        more_refined_df = refined_df[refined_df['User id'] == person]
        emojis = more_refined_df['Reaction'].values
        if person not in users:
            together = {}
            together['Message id'] = [message_id]
            together['User id'] = [person]
            together['Reaction'] = [value]
            df2 = pd.DataFrame(together)
            df = pd.concat([df,df2])
            df.to_csv("Reaction_Tracker.csv")
            point_df = pd.read_csv('Points.csv', index_col=[0])
            point_reciever = reaction.message.author.id
            points = point_df.loc[point_reciever]['Points']
            points = int(points) - 1
            point_df.at[person, "Points"] = points
            point_df.to_csv('Points.csv')
        elif 1007263123205533756 not in emojis:
            together = {}
            together['Message id'] = [message_id]
            together['User id'] = [person]
            together['Reaction'] = [value]
            df2 = pd.DataFrame(together)
            df = pd.concat([df,df2])
            df.to_csv("Reaction_Tracker.csv")
            point_df = pd.read_csv('Points.csv', index_col=[0])
            point_reciever = reaction.message.author.id
            points = point_df.loc[point_reciever]['Points']
            points = int(points) - 1
            point_df.at[person, "Points"] = points
            point_df.to_csv('Points.csv')            

@bot.command(name="check", help="Skill Check")
async def roll20(ctx):
    try:
        if ctx.message.author.bot:
            return
        str_list = ['Athletics','Strength']
        dex_list = ['Acrobatics','Stealth','Dexterity']
        con_list = ['Constitution']
        int_list = ['Acrcana','History','Investigation','Nature','Religion','Intelligence']
        wis_list = ['Animal Handling','Insight','Medicine','Perception','Survival','Wisdom']
        cha_list = ['Deception','Intimidation','Performance','Persuasion','Charisma']
        stat_list = [str_list,dex_list,con_list,int_list,wis_list,cha_list]
        size = len(stat_list)
        attribute_finder = random.randint(0, size -1)
        chosen_stat = stat_list[attribute_finder]
        stat_size = len(chosen_stat)
        stat_finder = random.randint(0,stat_size -1)
        chosen_val = chosen_stat[stat_finder]
        opponent_list = ['the Furlbogs','the Slimes','Joeseph Mother','Your Boss','An angry gnome','The divinity of pointlessness','The Bichealshop Quintet','The pope','The lord of the land',
        'the Goblins','a Deva','a knight','The Potion Seller','An Honest Merchant','Ghen Actis']
        opp_size = len(opponent_list)
        opponent_finder = random.randint(0,opp_size -1)
        opponent = opponent_list[opponent_finder]
        name = ctx.message.author.name
        result = random.randint(1,20)
        msg = f"{name} make a {chosen_val} check. \n"
        msg2 = f"You rolled a {result} \n"
        if result < 2:
            msg3 = f"You have failed your {chosen_val} check against {opponent}"
        elif result < 10:
            check =  [0,0,0,1]
            val = random.randint(0,len(check)-1)
            if val == 1:
                msg3 = f"You have passed your {chosen_val} check against {opponent}"
            else:
                msg3 = f"You have failed your {chosen_val} check against {opponent}"
        elif result < 16:
            check = [0,0,1,1]
            val = random.randint(0,len(check)-1)
            if val == 1:
                msg3 = f"You have passed your {chosen_val} check against {opponent}"
            else:
                msg3 = f"You have failed your {chosen_val} check against {opponent}"
        elif result <20:
            check = [0,1,1,1]
            val = random.randint(0,len(check)-1)
            if val == 1:
                msg3 = f"You have passed your {chosen_val} check against {opponent}"
            else:
                msg3 = f"You have failed your {chosen_val} check against {opponent}"
        elif result == 20:
            msg3 = f"You have passed your {chosen_val} check against {opponent}"
        await ctx.send(msg+msg2+msg3)
    except Exception as err:
        print(stat_finder)
        print(chosen_val)


# @bot.command(name='give_score', help='This gives you your friend a gamerscore \n')
# async def score_give(ctx):
#     if ctx.message.author.bot:
#         return
#     reply_message_id = ctx.message.reference.message_id
#     reply_message = await ctx.fetch_message(reply_message_id)
#     reply_author = reply_message.author
#     if reply_author == ctx.message.author:
#         await ctx.send("Sorry you can't give yourself points")
#     if ctx.message.reference is not None and reply_author != ctx.message.author:
#         text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#         name = text.author.name
#         name_id = text.author.id
#         point_df = pd.read_csv('Points.csv', index_col=[0])
#         points = point_df.loc[name_id]['Points']
#         points = int(points) + 1
#         point_df.at[name_id, "Points"] = points
#         point_df.to_csv('Points.csv')
#         await ctx.send(f"{name} you have {points} point(s). That is pretty poggers if I do say so myself.")

# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     msg = str(message.content)
#     check = "twitter.com"
#     check2 = "x.com"
#     check3 = "fxtwitter.com"
#     return_str = "before manipulation"
#     if check in msg or check2 in msg:
#         if check3 not in msg:
#             if check in msg:
#                 return_str = msg.replace(check, "fxtwitter.com")
#             elif check2 in msg:
#                 return_str = msg.replace(check2, "fxtwitter.com")
#             await message.channel.send(f'{return_str} FTFY')
#     await bot.process_commands(message)

bot.run(token)

