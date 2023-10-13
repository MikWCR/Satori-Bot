import asyncio
import urllib.request, json
import random
import os
import pytz
import re
import requests
import typing
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup, Comment
import typing
import discord
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle
from api.rotmgblog import BlogApi

intents = discord.Intents().all()
bot = commands.Bot(
  command_prefix='!', 
  intents=intents, 
  help_command=None,
  sync_commands=True)
initial_extensions = ['cogs.deathpoets']

  
@bot.event
async def on_ready():
    #global start_time
    #start_time = datetime.utcnow()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    for guild in bot.guilds:
        print("Connected to: " + guild.name)
    global guild_members
    guild = bot.get_guild(374716378655227914)
    guild_members = guild.members

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if message.guild.id == 153689763780624385:
        with open("root/Satori/info.json", "r") as f:
            users = json.load(f)
        
        await updatedata(users, message.author)
        await add_experience(users, message.author, message.content)
        await level_up(users, message.author, message)
                                    
        with open("root/Satori/info.json", "w") as fp:
            json.dump(users, fp, indent=4)

    lit = message.content
    if len(lit) < 1:
        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            print(f"[{str(message.created_at)}][{message.guild.name}][#{message.channel.name}] [{message.author.name}]{attachment.url}")
            return
        print(f"[{str(message.created_at)}][{message.guild.name}][#{message.channel.name}] [{message.author.name}] {message.content}")
        return

    print(f"[{str(message.created_at)}][{message.guild.name}][#{message.channel.name}] [{message.author.name}] {message.content}")
    
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    print(f"[MESSAGE DELETED][{message.guild.name}][{message.channel.name}][{message.author.name}] {message.content}")

@bot.event
async def on_message_edit(oldmsg, newmsg):
    if oldmsg.author == bot.user:
        return
    print(f"[EDITED MESSAGE][{oldmsg.guild.name}][{oldmsg.channel.name}][{oldmsg.author.name}] {oldmsg.content}\n--EDITED TO--\n{newmsg.content}")

@bot.event
async def on_member_remove(member):
    if member in guild_members:
        guild = bot.get_guild(374716378655227914)
        with open("root/Satori/logs.json", "r") as f:
            logs = json.load(f)
        logs[str(guild.id)]['Left Users'] += 1
        with open("root/Satori/logs.json", "w+") as fp:
            json.dump(logs, fp, indent=4)


    await ctx.send(embed=embed)


@bot.on_click(custom_id='epic_gamer')
async def gamer_role(i: discord.ComponentInteraction, button):
    role = discord.utils.get(i.guild.roles, name="Epic Gamer")
    if role in i.author.roles:
        await i.respond("Role removed.", hidden=True, delete_after=5.2)
        await i.author.remove_roles(role)
    else:
        await i.respond("Added epic gamer role.", hidden=True, delete_after=5.2)
        await i.author.add_roles(role)
@bot.on_click(custom_id='nsfw_button')
async def nsfw_role(i: discord.ComponentInteraction, button):
    role = discord.utils.get(i.guild.roles, name="nsfw")
    if role in i.author.roles:
        await i.respond("Role removed.", hidden=True, delete_after=5)
        await i.author.remove_roles(role)
    else:
        await i.respond("Added nsfw role. Enjoy... weirdo.", hidden=True, delete_after=5)
        await i.author.add_roles(role
       

async def updatedata(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['Name'] = user.name
        users[str(user.id)]['Exp'] = 0
        users[str(user.id)]['Level'] = 1
        users[str(user.id)]['Currency'] = 100


async def level_up(users, user, message):
    experience = users[str(user.id)]['Exp']
    lvl_start = users[str(user.id)]['Level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end} and has earned 100 ₘᵤₙₙᵢₑₛ')
        users[str(user.id)]['Level'] = lvl_end
        users[str(user.id)]['Currency'] += 100


async def add_experience(users, user, content):
    if content.startswith("!"):
        return
    r = random.randint(4, 13)
    users[str(user.id)]['Exp'] += r
    #bal = users[str(user.id)]['Currency']

async def start_logs(message):
    #date of log starting 9/2/22
    with open("root/Satori/logs.json", "r") as f:
        logs = json.load(f)
    if not str(message.guild.id) in str(logs):
        logs[str(message.guild.id)] = {}
        logs[str(message.guild.id)]['Accepted Applications'] = 0
        logs[str(message.guild.id)]['Declined Applications'] = 0
        logs[str(message.guild.id)]['Left Users'] = 0
        logs[str(message.guild.id)]['Error Applying Role'] = 0

        with open("root/Satori/logs.json", "w+") as fp:
             json.dump(logs, fp, indent=4)
        
if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)
  bot.run(TOKEN)
