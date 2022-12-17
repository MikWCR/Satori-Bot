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
initial_extensions = ['cogs.owner', 'cogs.nsfw', 'cogs.deathpoets', 'cogs.test', 'cogs.econ', 'cogs.pins']

        #big nut!
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

    if message.content.lower() == "top":
        await message.channel.send("kek")
    if message.content.lower() == "gay":
        await message.channel.send("haha u gay")
    # if "uwu" in message.content.lower():
    #     await message.channel.send("uwu daddy uwu sussy amongus")
    # triggers = ["among", "amogus"]
    # sus = ["https://i.ytimg.com/vi/PhFOch6beiE/maxresdefault.jpg", "https://i.pinimg.com/originals/9b/62/c8/9b62c81a608fea5076471365d852cb18.jpg"]
    # if any(x in message.content.lower() for x in triggers):
    #     await message.channel.send("amonus 😩")
    #     await message.channel.send(random.choice(sus))
    
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

@bot.command(pass_context=False)
async def help(ctx):
    #make a help command
    embed = discord.Embed(title="Help", description="", color=0x00ff00)
    embed.add_field(name="!ping", value="Returns pong", inline=False)
    embed.add_field(name="!help", value="Returns this message", inline=False)
    embed.add_field(name="!say", value="Makes the bot say something", inline=False)
    embed.add_field(name="!purge", value="Deletes a certain amount of messages", inline=False)
    embed.add_field(name="!pins", value="Shows latest pins for current server. React with 📌 to pin messages", inline=False)
    embed.add_field(name="!pins (pin number)", value="Shows a pin of your choice if any are found. React with 📌 to pin messages", inline=False)
    embed.add_field(name="!pins search (param)", value="Searches through pins based on your input.", inline=False)
    #embed.add_field(name="Gambling", value="", inline=False)
    #embed.add_field(name="!bal", value="Shows your current balance. (Only if level system is active on server)", inline=False)
    embed.add_field(name="!yandere", value="Grabs random images from yande.re. (nsfw)", inline=False)

    
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    #make a help command
    embed = discord.Embed(title="Server Info", description="", color=0x00ff00)
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Server Owner", value=ctx.guild.owner, inline=False)
    embed.add_field(name="Server Region", value=ctx.guild.region, inline=False)
    embed.add_field(name="Server Verification Level", value=ctx.guild.verification_level, inline=False)
    embed.add_field(name="Server Member Count", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Server Created At", value=str(ctx.guild.created_at), inline=False)
    embed.add_field(name="Server Icon", value=ctx.guild.icon_url, inline=False)
    embed.add_field(name="Server Emojis", value=ctx.guild.emojis, inline=False)
    embed.add_field(name="Server Roles", value=ctx.guild.roles, inline=False)
    embed.add_field(name="Server Channels", value=ctx.guild.channels, inline=False)
    embed.add_field(name="Server Features", value=ctx.guild.features, inline=False)
    embed.add_field(name="Server Splash", value=ctx.guild.splash_url, inline=False)

    await ctx.send(embed=embed)
    #await ctx.send(embed=embed, components=components)
    


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
        await i.author.add_roles(role)
@bot.command(pass_context=True)
async def pix(ctx, s=""):
     _TOKEN = "cdy-iQjYHPEiggQlTC_eKREwMMCFgRUeoMwgo9iFOtk"
     if "https://www.pixiv.net/en/artworks/" in s:
        artwork = re.findall("\d+", s)[0]
        print(artwork)
    #  async with PixivClient() as client:
    #     aapi = AppPixivAPI(client=client)
    #     try:
    #         await aapi.login(refresh_token=_TOKEN)
    #     except:
    #         await ctx.send("Unable to login to pixiv.")
    #         return
    #     illust_detail = await aapi.illust_detail(artwork)
        #print(illust_detail)
        #json_result = await aapi.illust_ranking()
            #print(illust.user.name)
        #await aapi.download(illust_detail['illust']['image_urls']['large'])

@bot.command(pass_context=True)
async def realmeye(ctx, *arg):
    url = "https://www.realmeye.com/forum/c/news.json"
    headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as url:
        eye_data = json.loads(url.read().decode())
    print(eye_data["0"])
            

# @bot.command(aliases=["balance", "b"], pass_context=True)
# async def bal(ctx, user=""):
#     with open("root/Satori/info.json", "r") as f:
#         users = json.load(f)
#     if not user:                                                                                                
#         currency = users[str(ctx.message.author.id)]['Currency']
#         await ctx.send(f"Balance: {currency} ₘᵤₙₙᵢₑₛ")
#     else:
#         try:
#             mentionid = re.findall(r'\b\d+\b', user)
#             userbal = users[str(mentionid[0])]['Currency']
#             await ctx.send(f"{user}'s balance: {userbal}")
#         except:
#             await ctx.send("User not found in database. Most likely never spoke or a mf robot.")
#             return

@bot.command(pass_context=True)
async def coinflip(ctx, amount="", choice=""):
    if int(amount) <= 0:
        return
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    dte = ctx.message.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))
    if not amount:
        amount = 100
        message = await ctx.send("You are betting 100. Are you ok with this?")
        await message.add_reaction("✅")
        await message.add_reaction("🚫")
        try:
            reaction, user = await bot.wait_for("reaction_add",
            check=lambda reaction, 
            user: user == ctx.author and reaction.emoji in ["✅", "🚫"],
            timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out waiting for response. Coin flip cancelled.")
            return
        else:
            if reaction.emoji == "✅":
                if not choice:
                    secmsg = await ctx.send("Heads are tails?")
                    def echeck(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    try:
                        msg = await bot.wait_for('message', check=echeck, timeout = 20.0)
                    except asyncio.TimeoutError:
                        await ctx.send("Timed out waiting for response. Pick a fuckin side stop doin that shit")
                    else:
                        choice = msg.content.lower()
                        if choice == "tails":
                            await coin_flip_game(choice, amount, channel=ctx.message.channel.id, date=dte, author=ctx.message.author.id)
                            return
                        elif choice =="heads":
                            await coin_flip_game(choice, amount, channel=ctx.message.channel.id, date=dte, author=ctx.message.author.id)
                            return
                        else:
                            await ctx.send("Pick a side next time will ya.")
                            return
            else:
                await ctx.send("Coin flip cancelled.")
                return
    else:
        if not choice:
            secmsg = await ctx.send("Heads are tails?")
            def echeck(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            try:
                msg = await bot.wait_for('message', check=echeck, timeout = 20.0)
            except asyncio.TimeoutError:
                await ctx.send("Timed out waiting for response.")
            else:
                choice = msg.content.lower()
                if choice == "tails":
                    await coin_flip_game(choice, amount, channel=ctx.message.channel.id, date=dte, author=ctx.message.author.id)
                    return
                elif choice =="heads":
                    await coin_flip_game(choice, amount, channel=ctx.message.channel.id, date=dte, author=ctx.message.author.id)
                    return
                else:
                    await ctx.send("Pick a side next time will ya.")
                    return
        elif choice and amount:
            if choice == "tails" or choice == "heads":
                ################################
                # if current_bal < int(amount):
                #     await ctx.send("Not enough ₘᵤₙₙᵢₑₛ. Level up to get more or use the stock market.")
                #     return
                ################################
                await coin_flip_game(choice, amount, channel=ctx.message.channel.id, date=dte, author=ctx.message.author.id)
                return
            else:
                await ctx.send("Pick a side mf.")
                return

# @commands.cooldown(1.0, 3.0, commands.BucketType.guild)
# @bot.command(pass_context=False, aliases=["fishing", "f"])
# async def fish(ctx):
#     emb = await fish_game(ctx) 
#     components = [ActionRow(Button(label='Fish Again',
#                                custom_id='fish_button',
#                                style=ButtonStyle.green
#                                ),
#                         Button(label='Sell',
#                                custom_id='sell_button',
#                                style=ButtonStyle.green),
#                         Button(label='Shop',
#                                custom_id='shop_button',
#                                style=ButtonStyle.green,
#                                disabled=True))
#               ]
#     await ctx.send(embed=emb, components = components)
#     try:
#         while True:

#             interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button1")
#             newemb = await fish_game(ctx)
#             await interaction.edit(embed=newemb, components = components)
#         #await ctx.send(embed=newemb, components = [Button(style=1, label="Fish", custom_id = "button1"), Button(style=1, label="Shop", custom_id = "button2")])
#         #await interaction.send(embed=newemb, components = [Button(style=3, label="Fish", custom_id = "button1"), Button(style=3, label="Shop", custom_id = "button2")])
#     except Exception as e:
#         print(e)
        
#     # elif fishing[str(ctx.message.author.id)]['rod'] == "advanced":
#     #     if random.randint(1, 100) <= 50:
#     #         fish_type = random.choice(advanced_fish_types)


@bot.command()
async def button(ctx):
    await ctx.message.delete()
    #Styles
    #1: Blurple. 2: Grey, 3: Green, 4: Red, 5: Grey with URL.
    msg = await ctx.send("Test button", components = [Button(style=3, label="HOLY SHIT A BUTTON!", custom_id = "button1")])
    interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button1")
    #await msg.edit("w3owow", components = [])
    #await interaction.edit_origin(components = [])
    await interaction.send(content = "Button clicked!")

@bot.command(pass_context=True, aliases=["inv", "i"])
async def inventory(ctx):
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    with open("root/Satori/farm.json", "r") as fp:
        farm = json.load(fp)
    embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", description="", color=0x00ff00)
    if not farm[str(ctx.message.author.id)]:
        embed.description = "You're inventory is empty! Use !shop to buy stuff!"
        await ctx.send(embed=embed)
        return
    else:
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Seeds", value="\n".join([f"{k}: {v}" for k, v in farm[str(ctx.message.author.id)]['seeds'].items()]), inline=False)
        embed.set_footer(text="Use !shop to buy seeds.")
        await ctx.send(embed=embed)
    
@bot.command()
async def shop(ctx):
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    with open("root/Satori/farm.json", "r") as fp:
        farm = json.load(fp)
    if not str(ctx.message.author.id) in str(farm):
        await new_farmer(ctx)
        
    seed_types = ["grain", "wheat", "corn"]
    sapling_types = ["oak", "pine", "maple"]
    components = [ActionRow(Button(label='Seeds',
                               custom_id='rods_button',
                               style=ButtonStyle.blurple
                               ),
                            Button(label="Saplings",
                                    custom_id="saplings_button",
                                    style=ButtonStyle.blurple),
                            Button(label='Equipment',
                                custom_id='boats_button',
                                style=ButtonStyle.blurple))]
    embed = discord.Embed(title=f"Shop for all your farming needs.", description="**/shop seeds**: Good for starting out.\n **/shop saplings**: Plant them trees and get hella cash.", color=0x00ff00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text="Use !inv to view your inventory.")
    await ctx.send(embed=embed, components = components)
    

    
@bot.command()
async def plant(ctx, seed: str, amount: int):
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    with open("root/Satori/farm.json", "r") as fp:
        farm = json.load(fp)
    inventory = farm[str(ctx.message.author.id)]['inventory']['seeds']
    if not seed in farm[str(ctx.message.author.id)]['seeds']:
        await ctx.send("You don't have that seed!")
        return
     
    return
async def new_farmer(ctx):
    with open("root/Satori/farm.json", "r") as fp:
        farm = json.load(fp)
    farm[str(ctx.message.author.id)] = {}
    farm[str(ctx.message.author.id)]['inventory'] = {}
    farm[str(ctx.message.author.id)]['inventory']['seeds'] = {}
    farm[str(ctx.message.author.id)]['inventory']['seeds']['grain'] = 0
    farm[str(ctx.message.author.id)]['inventory']['seeds']['wheat'] = 0
    farm[str(ctx.message.author.id)]['inventory']['seeds']['corn'] = 0
    farm[str(ctx.message.author.id)]['inventory']['saplings'] = {}
    farm[str(ctx.message.author.id)]['inventory']['saplings']['oak'] = 0
    farm[str(ctx.message.author.id)]['inventory']['saplings']['pine'] = 0
    farm[str(ctx.message.author.id)]['inventory']['saplings']['maple'] = 0
    farm[str(ctx.message.author.id)]['planted'] = False
    farm[str(ctx.message.author.id)]['planted_time'] = 0
    with open("root/Satori/farm.json", "w") as fp:
        json.dump(farm, fp, indent=4)


@bot.command()
async def fishshop(ctx):
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    with open("root/Satori/fishing.json", "r") as fp:
        fishing = json.load(fp)
    print(fishing)
    inventory = fishing[str(ctx.message.author.id)]
    components = [ActionRow(Button(label='Rods',
                               custom_id='rods_button',
                               style=ButtonStyle.green
                               ),
                        Button(label='Boats',
                               custom_id='boats_button',
                               style=ButtonStyle.green))
              ]
    bal = users[str(ctx.message.author.id)]['Currency']
    print(bal)
    embed = discord.Embed(title="Shop", description="Buy fishing equipment here!", color=0x00ff00)
    embed.set_author(name=f"{ctx.message.author.name}'s balance: {bal} ₘᵤₙᵢₑₛ.", icon_url="http://www.minecraftguides.org/wp-content/uploads/2012/07/fishR.gif")
    msg = await ctx.send(embed=embed, components = components)
    
    def _check(i: discord.ComponentInteraction, b):
        return i.message == msg and i.member == ctx.author
    interaction, button = await bot.wait_for('button_click', check=_check)
    button_id = button.custom_id
    if button_id == "rods_button":

        new_components = [ActionRow(Button(style=ButtonStyle.green,
                                     label="Buy Plastic Rod",
                                      custom_id = "plastin_button"), 
                                    Button(style=ButtonStyle.green,
                                     label="Buy Advanced Fishing Rod",
                                      custom_id = "advanced_button"),
                                    Button(style=ButtonStyle.green,
                                     label="Buy Legendary Fishing Rod",
                                      custom_id = "legendary_button"), 
                                    Button(style=ButtonStyle.green,
                                     label="Buy Master Fishing Rod",
                                      custom_id = "master_button"), 
                                    Button(style=ButtonStyle.green,
                                     label="Back",
                                      custom_id = "back"))]

        if inventory['rod'] == "plastic":
            new_components[0][0].label = "Selected"
            new_components[0][0].disabled = True
            new_components[0][0].style = ButtonStyle.blurple
            embed.add_field(name="Rods",
                value="Plastic Rod: Selected\nAdvanced Rod: 3000\nLegendary Rod: 10000\nMaster Rod: 25000",
                inline=False) 
        elif inventory['rod'] == "advanced":
            for i in range(1):
                new_components[0].disable_component_at(i)
            new_components[0][1].label = "Selected"
            new_components[0][1].style = ButtonStyle.blurple
            embed.add_field(name="Rods", 
                value="Plastic Rod: OWNED\nAdvanced Rod: Selected\nLegendary Rod: 10000\nMaster Rod: 25000",
                inline=False)
        elif inventory['rod'] == "legendary":
            for i in range(2):
                new_components[0].disable_component_at(i)
            new_components[0][2].label = "Selected"
            new_components[0][2].style = ButtonStyle.blurple
            embed.add_field(name="Rods", 
                value="Plastic Rod: OWNED\nAdvanced Rod: OWNED\nLegendary Rod: Selected\nMaster Rod: 25000",
                inline=False)
        elif inventory['rod'] == "master":
            for i in range(3):
                new_components[0].disable_component_at(i)
            new_components[0][3].label = "Selected"
            new_components[0][3].style = ButtonStyle.blurple
            embed.add_field(name="Rods", 
                value="Plastic Rod: OWNED\nAdvanced Rod: OWNED\nLegendary OWNED: OWNED\nMaster Rod: Selected",
                inline=False)
        else:
            embed.add_field(name="You have a basic rod. Save some money and upgrade!",
                value="Plastic Rod: 300\nAdvanced Rod: 3000\nLegendary Rod: 10000\nMaster Rod: 25000",
                inline=False)
        await interaction.defer()  
        await interaction.edit(embed=embed, components=new_components)
        while True:
            interactionI, buttonI = await bot.wait_for('button_click', check=_check)
            button_id1 = buttonI.custom_id
            
            if button_id1 == "plastin_button":
                if bal < 300:
                    await interaction.defer()  
                    await interactionI.edit(embed=embed.add_field(name="Error", value="You do not have enough money to buy this item.", inline=False))
                    return
                else:
                    #change 
                    new_components[0][0].label = "OWNED"
                    new_components[0][0].disabled = True
                    new_components[0][0].style = ButtonStyle.blurple
                    new_emb = discord.Embed(title="Shop", description="Buy fishing equipment here!", color=0x00ff00)
                    new_emb.set_author(name=f"{ctx.message.author.name}'s balance: {bal - 300} ₘᵤₙᵢₑₛ.", icon_url="http://www.minecraftguides.org/wp-content/uploads/2012/07/fishR.gif")
                    new_emb.add_field(name="Rods",
                        value="Plastic Rod: OWNED\nAdvanced Rod: 3000\nLegendary Rod: 10000\nMaster Rod: 25000",
                        inline=False)  
                    await interactionI.defer()  
                    await interactionI.edit(embed=new_emb.add_field(name="Plastic Rod", value="Bought!", inline=False),
                    components = new_components)
                    users[str(ctx.message.author.id)]['Currency'] -= 300
                    inventory['rod'] = "plastic"
            elif button_id1 == "advanced_button":
                if bal < 3000:
                    await interaction.defer()  
                    await interactionI.edit(embed=embed.add_field(name="Error", value="You do not have enough money to buy this item.", inline=False))
                    
                else:
                    #change 
                    new_components[0][1].label = "OWNED"
                    new_components[0][1].style = ButtonStyle.blurple
                    new_components[0][1].disabled = True
                    await interactionI.defer()
                    await interactionI.edit(embed=embed.add_field(name="Advanced Rod", value="Bought!", inline=False),
                    components = new_components)
                    users[str(ctx.message.author.id)]['Currency'] -= 3000
                    inventory['rod'] = "advanced"
            elif button_id1 == "legendary_button":
                if bal < 10000:
                    await interaction.defer()  
                    await interactionI.edit(embed=embed.add_field(name="Error", value="You do not have enough money to buy this item.", inline=False))
                
                else:
                    #change 
                    new_components[0][2].label = "OWNED"
                    new_components[0][2].style = ButtonStyle.blurple
                    new_components[0][2].disabled = True
                    await interactionI.defer()
                    await interactionI.edit(embed=embed.add_field(name="Legendary Rod", value="Bought!", inline=False),
                    components = new_components)
                    users[str(ctx.message.author.id)]['Currency'] -= 10000
                    inventory['rod'] = "legendary"
            elif button_id1 == "master_button":
                if bal < 25000:
                    await interaction.defer()  
                    await interactionI.edit(embed=embed.add_field(name="Error", value="You do not have enough money to buy this item.", inline=False))
                    
                else:
                    #change 
                    new_components[0][3].label = "OWNED"
                    new_components[0][3].style = ButtonStyle.blurple
                    new_components[0][3].disabled = True
                    await interactionI.defer()
                    await interactionI.edit(embed=embed.add_field(name="Master Rod", value="Bought!", inline=False),
                    components = new_components)
                    users[str(ctx.message.author.id)]['Currency'] -= 25000
                    inventory['rod'] = "master"

            with open("root/Satori/info.json", "w") as f:
                json.dump(users, f, indent=4)
            with open("root/Satori/fishing.json", "w") as fp:
                json.dump(fishing, fp, indent=4)

            # if button_id1 == "plastin_button":
            #     if bal < 300:
            #         await interactionI.send("You don't have enough money!")
            #         return
            #     users[str(ctx.message.author.id)]['Currency'] -= 300
            #     fishing[str(ctx.message.author.id)]['rod'] = "plastic"
            #     await interactionI.send("You bought a plastic fishing rod!")
            # elif button_id1 == "advanced_button":
            #     if bal < 3000:
            #         await interactionI.send("You don't have enough money!")
            #         return
            #     users[str(ctx.message.author.id)]['Currency'] -= 3000
            #     fishing[str(ctx.message.author.id)]['rod'] = "advanced"
            #     await interactionI.send("You bought an advanced fishing rod!")
            # elif button_id1 == "legendary_button":
            #     if bal < 10000:
            #         await interactionI.send("You don't have enough money!")
            #         return
            #     users[str(ctx.message.author.id)]['Currency'] -= 10000
            #     fishing[str(ctx.message.author.id)]['rod'] = "legendary"
            #     await interactionI.send("You bought a legendary fishing rod!")
            # elif button_id1 == "master_button":
            #     if bal < 25000:
            #         await interactionI.send("You don't have enough money!")
            #         return
            #     users[str(ctx.message.author.id)]['Currency'] -= 25000
            #     fishing[str(ctx.message.author.id)]['rod'] = "master"
            #     await interactionI.send("You bought a master fishing rod!")
            # elif button_id1 == "back":
            #     await interactionI.send("You went back to the shop!")
            #     await shop(ctx)
        # if button_id == "boats_button":
        #     boat_components = [ActionRow(
        #                                  Button(style=ButtonStyle.green, label = "Fishing Boat", custom_id = "fboat_button"),
        #                                  Button(style=ButtonStyle.green, label = "Sailboat", custom_id = "sail_button"),
        #                                  Button(style=ButtonStyle.green, label = "Yacht", custom_id = "yacht_button"),
        #                                  Button(style=ButtonStyle.green, label = "Back", custom_id = "back"))]
        #     await interaction.edit(embed=embed.add_field(name="Rods", 
        #                             value="Fishing Boat: 5000\nSailboat: 20000\nYacht: 40000\n", inline=False),
        #                             components = boat_components)

    # interactionII = await bot.wait_for("button_click", check = lambda i: i.custom_id == "button2")
    # interactionII.say("You clicked the back button!")


# @bot.command(pass_context=True, aliases=["stonks", "s", "stocks"])
# async def stock(ctx):
#     with open("stocks.json", "r") as f:
#         stocks = json.load(f)
#     if len(stocks) < 1:
#         return
        
# @bot.command(pass_context=True, aliases=["addstock", "as"])
# async def add_stock(ctx, stock_name, stock_price: int):
#     with open("stocks.json", "r") as f:
#         stocks = json.load(f)
#     if not stock_name:
#         await ctx.send("Please enter a stock name!")
#         return
#     if not stock_price:
#         await ctx.send("Please enter a stock price!")
#         return
#     if not stock_name in stocks:
#         stocks = {}
#         stocks[stock_name] = {}
#         stocks[stock_name]['full_name'] = "FULL NAME HERE ON INPUT"
#         stocks[stock_name]['price'] = stock_price
#         stocks[stock_name]['total'] = 0




async def fish_game(ctx):
    basic_fish_types = ["fish", "salmon", "cod"]
    advanced_fish_types = ["monkfish", "tropical_fish", "pufferfish"]
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    with open("root/Satori/fishing.json", "r") as fp:
        fishing = json.load(fp)
    if not str(ctx.message.author.id) in str(fishing):
        #update user info into file
        fishing[str(ctx.message.author.id)] = {}
        fishing[str(ctx.message.author.id)]['rod'] = "basic"
        fishing[str(ctx.message.author.id)]['boat'] = "rowboat"
        fishing[str(ctx.message.author.id)]['inventory'] = {}
        fishing[str(ctx.message.author.id)]['inventory']['fish'] = 0
        fishing[str(ctx.message.author.id)]['inventory']['salmon'] = 0
        fishing[str(ctx.message.author.id)]['inventory']['cod'] = 0
        with open("root/Satori/fishing.json", "w") as fp:
            json.dump(fishing, fp, indent=4)
        await ctx.send("You have been given a basic fishing rod and a rowboat. Use `!inventory` to see your inventory.")
    dte = ctx.message.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))
    emb = discord.Embed(title="You went fishing!", description="", color=0x00ff00)
    emb.set_author(name=f"{ctx.message.author.name}", icon_url="http://www.minecraftguides.org/wp-content/uploads/2012/07/fishR.gif")
        # total fish caught

    if fishing[str(ctx.message.author.id)]['rod'] == "basic":
        caught_fish = random.randint(4, 8)
        caught_cod =  random.randint(2, 5)
        caught_salmon = random.randint(0, 3)
        total_fish = caught_fish + caught_cod + caught_salmon
        r_exp = round(total_fish * 2.34)
            
        if caught_salmon > 0:
            emb.add_field(name="You caught:", value=f"Fish: {caught_fish}\nCod: {caught_cod}\nSalmon: {caught_salmon}", inline=False)
        else:
            emb.add_field(name="You caught:", value=f"Fish: {caught_fish}\nCod: {caught_cod}", inline=False)
        emb.add_field(name="You gained:", value=f"{r_exp} EXP", inline=False)
        if random.randint(1, 100) >= 85:
            r = random.randint(35, 70)
            emb.add_field(name="You found a common chest!", value=f"Chest contained {r} ₘᵤₙᵢₑₛ ", inline=False)
            #update currency in info
            users[str(ctx.message.author.id)]['Currency'] += r
        #update data
        exp_gain = r_exp * total_fish
        users[str(ctx.message.author.id)]['Exp'] += r_exp
        fishing[str(ctx.message.author.id)]['inventory']['fish'] += caught_fish
        fishing[str(ctx.message.author.id)]['inventory']['cod'] += caught_cod
        fishing[str(ctx.message.author.id)]['inventory']['salmon'] += caught_salmon
        with open(file="root/Satori/info.json", mode="w") as f:
            json.dump(users, f, indent=4)
        with open(file="root/Satori/fishing.json", mode="w") as fp:
            json.dump(fishing, fp, indent=4)
        return emb


async def coin_flip_game(choice, amount, channel, date, author):
    with open("root/Satori/info.json", "r") as f:
        users = json.load(f)
    current_bal = users[str(author)]['Currency']
    chan = await bot.fetch_channel(channel)
    if current_bal < int(amount):
        await chan.send("Not enough ₘᵤₙᵢₑₛ. Level up to get more or use the stock market.")
        return
    results = ["https://c.tenor.com/kK8D7hQXX5wAAAAC/coins-tails.gif", 
                    "https://c.tenor.com/nEu74vu_sT4AAAAC/heads-coinflip.gif"]
    r = random.randint(0, 50)
    print(r)
    dte = date.strftime("%m/%d/%Y, %H:%M:%S")
    embed = discord.Embed(title=f"You have chosen {choice}.", color=0xbd9e15)
    embed.set_author(name=f"Coinflip for {amount}.", icon_url="https://www.iconpacks.net/icons/1/free-heads-or-tails-icon-456-thumb.png")
    embed.set_footer(text=f'{dte}')
    if r < 25:
        #tails
        answer = results[0]
        embed.set_image(url=answer)
        await chan.send(embed=embed)
    else:
        #heads
        answer = results[1]
        embed.set_image(url=answer)
        await chan.send(embed=embed)
    await asyncio.sleep(2)
    bal = users[str(author)]["Currency"]
    if choice in answer:
        users[str(author)]["Currency"] += int(amount)
        bal = users[str(author)]["Currency"]
        await chan.send(f"You have won {amount} ₘᵤₙᵢₑₛ! You're new total is {bal}.")
    else:
        users[str(author)]["Currency"] -= int(amount)
        bal = users[str(author)]["Currency"]
        await chan.send(f"You lost {amount} ₘᵤₙᵢₑₛ! You're total is {bal}.")
    with open("root/Satori/info.json", "w") as fp:
        json.dump(users, fp, indent=4)
        

#async def realmblog(post=0):
    # blog = BlogApi()
    # i = 0
    # r = random.randint(0, 0xffffff)
    # content = await blog.content(post)
    # content = re.sub('([A-Z])', r' \1', content)
    # title, url, date = await blog.title(thread=post), await blog.url(thread=post), await blog.date(thread=post)
    # images = await blog.images(thread=post)
    # with open("root/Satori/latest.json", "r") as f:
    #     latest = json.load(f)
    # try:
    #     if not latest['channel']:
    #         print("Channel not set")
    #         return
    # except:
    #     print("No channel set <>!")
    #     return
    # channel = str(latest['channel'])
    # rchannel = await bot.fetch_channel(channel)
    # if not "post" in latest:
    #     latest['post'] = ""
    # if not content in latest['post']:
    #     latest["post"] = content
    #     #get 2000 characters in the post
    #     if len(content) > 1995:
    #         content = content[:1995] + "[...]"
    #     else:
    #         content = content + "[...]"
    #     embed = discord.Embed(title=f"{title}", description=f"{content}", color=r)
    #     embed.set_author(name=f"Click here to view the rest of the post!", url=f"{url}", icon_url="https://remaster.realmofthemadgod.com/favicon.png")
    #     embed.set_footer(text=f"Date posted: {date}")
    #     try:
    #         embed.set_image(url=images[0])
    #     except:
    #         pass
    #     await rchannel.send(embed=embed)
    #     with open("root/Satori/latest.json", "w") as f:
    #         json.dump(latest, f, indent=4)
################################################################################
# THIS RIGHT HERE POSTS ALl OF THE BLOG POST NOT JUST ONE EMBED BUT IS BUGGY #
        # char = content.split("\n")
        # send_str = ""
    #     for line in char:
    #         if len(send_str) + len(line) > 1998:
    #             try:
    #                 embed = discord.Embed(title=f"{url}", description=f"{send_str}", color=r)
    #                 embed.set_author(name=f"{title}", url=f"{url}", icon_url="https://remaster.realmofthemadgod.com/favicon.png")
    #                 embed.set_footer(text=f"Date posted: {date}")
    #                 try:
    #                     embed.set_image(url=images[0])
    #                 except:
    #                     continue
    #                 await rchannel.send(embed=embed)
    #             except:
    #                 print("error for some reason")
    #             send_str = ""
    #         send_str += line + "\n"
    #     if send_str:
    #         try:
    #             embed = discord.Embed(title=f"{url}", description=f"{send_str}", color=r)
    #             embed.set_author(name=f"{title}", url=f"{url}", icon_url="https://remaster.realmofthemadgod.com/favicon.png") 
    #             embed.set_footer(text=f"Date posted: {date}")
    #             try:
    #                 for i in images:
    #                     embed.set_image(url=i)
    #                 #embed.set_image(url=images[0])
    #             except:
    #                 print("No iamges")
                    
    #             await rchannel.send(embed=embed)
    #         except:
    #             print('another error for some reason')
    #     with open("latest.json", "w") as fp:
    #         json.dump(latest, fp, indent=4)
    # else:
    #     #print("This blog post has already been posted.")
    #     return
 ################################################################################   

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
    # if not logs[str(message.guild.id)]['Users']:
    #     logs[str(message.guild.id)]['Users'] = {}
    #     staff_role = discord.utils.get(message.guild.roles, name="Staff")
    #     leader_role = discord.utils.get(message.guild.roles, name="Leader")
    #     founder_role = discord.utils.get(message.guild.roles, name="Founder")
    #     for x in message.guild.members:
    #         if staff_role or leader_role or founder_role in x:
    #             print(x)
            #logs[str(message.guild.id)]['Users']
        # Get all members who have Staff role, and log them into file wnd how many applications theyve denied or accepted

        with open("root/Satori/logs.json", "w+") as fp:
             json.dump(logs, fp, indent=4)
        
if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)
  bot.run(TOKEN)
