from api.rotmgblog import BlogApi
from discord.ext import tasks, commands
import discord
from discord import SlashCommandOption as Option, Localizations, Permissions, ApplicationCommandInteraction as APPCI, emoji
from discord import ComponentInteraction, ModalSubmitInteraction, Modal, TextInput, Button, ButtonStyle, SelectMenu, SelectOption
from discord import ActionRow
from typing import Optional, List

import random
import urllib.request, json
import asyncio
import random
import re
from datetime import datetime
from datetime import date
import numpy as np
import logging




class DeathPoetsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        global emojis, descriptions
        emojis = {
            'Life': '<:life:1033436223261392916>',
            'Mana': '<:mana:1033436224372871339>',
            'Att': '<:att:1033436220417650798>',
            'Spd': '<:spd:1033436225299816558>',
            'Vit': '<:vit:1033436226553905193>',
            'Def': '<:def:1033436221453635594>',
            'Dex': '<:dex:1033436222330249346>',
            'Wis': '<:wis:1033436227896098856>',
            'Ubhp': '<:ubhp:1035524115198656553>',
            'Deca': '<:decaring:1035524113747411016>',
            'Dominion': '<:t14armor:1035523462208430181>',
            'Wyrmhide': '<:wyrmhide:1038478552733065317>',
            'Star-Mother': '<:starmother:1038478551520915557>',
            'Vital-Unity': '<:t13staff:1035523460602007593>',
            'Sinister-Deeds': '<:sinisterdeeds:1038479245413982228>',
            'Mystical-Energy': '<:mysticalenergy:1038479243312640020>',
            'Evocation': '<:evocation:1038479330944237679>',
            'Splendor': '<:splendor:1038479246491910174>',
            'Sadamune': '<:sadamune:1038479244315086848>'

        }
        descriptions = {
                    'Vital-Unity': 'T13 Staff',
                    'Splendor': 'T13 Sword',
                    'Mystical-Energy': 'T13 Bow',
                    'Sinister-Deeds': 'T13 Dagger',
                    'Evocation':'T13 Wand',
                    'Sadamune':'T13 Katana',
                    'Dominion':'T14 Heavy Armor',
                    'Wyrmhide':'T14 Leather',
                    'Star-Mother':'T14 Robe'             
                }
    def cog_unload(self):
        self.realmblog_loop.cancel()

    @commands.Cog.on_click(custom_id='epic_gamer')
    async def gamer_role(self, i: discord.ComponentInteraction, button):
        role = discord.utils.get(i.guild.roles, name="Epic Gamer")
        if role in i.author.roles:
            await i.respond("Role `Epic Gamer` removed.", hidden=True, delete_after=5.2)
            await i.author.remove_roles(role)
        else:
            await i.respond("Added `Epic Gamer` role.", hidden=True, delete_after=5.2)
            await i.author.add_roles(role)
    @commands.Cog.on_click(custom_id='nsfw_button')
    async def nsfw_role(self, i: discord.ComponentInteraction, button):
        role = discord.utils.get(i.guild.roles, name="nsfw")
        if role in i.author.roles:
            await i.respond("Role `nsfw` removed.", hidden=True, delete_after=5)
            await i.author.remove_roles(role)
        else:
            await i.respond("Added `nsfw` role. Enjoy... weirdo.", hidden=True, delete_after=5)
            await i.author.add_roles(role)
    @commands.Cog.on_click(custom_id='o3_role')
    async def o3_role(self, i: discord.ComponentInteraction, button):
        role = discord.utils.get(i.guild.roles, name="O3")
        if role in i.author.roles:
            await i.respond("Role `O3` removed.", hidden=True, delete_after=5)
            await i.author.remove_roles(role)
        else:
            await i.respond("Added `O3` role.", hidden=True, delete_after=5)
            await i.author.add_roles(role)
    @commands.Cog.on_click(custom_id='shats_role')
    async def shats_role(self, i: discord.ComponentInteraction, button):
        role = discord.utils.get(i.guild.roles, name="Shatters")
        if role in i.author.roles:
            await i.respond("Role `Shatters` removed.", hidden=True, delete_after=5)
            await i.author.remove_roles(role)
        else:
            await i.respond("Added `Shatters` role.", hidden=True, delete_after=5)
            await i.author.add_roles(role)

    @commands.Cog.listener()
    async def on_ready(self):
        self.realmblog_loop.start()
        
        # if raffle_settings:
        #     names = []
        #     for user_id, user_settings in raffle_settings.items():
        #         try:
        #             names.append(user_settings['Name'])
        #         except Exception as e:
        #             print(e)
        #             continue
        global pots, items, armors, weapons
        with open("root/Satori/raffle_settings.json", "r") as f:
            raffle_settings = json.load(f)

        pots = ['Life', 'Mana', 'Att', 'Def', 'Spd', 'Dex', 'Wis', 'Vit']

        items = ['Ubhp','Deca','Dominion', 'Wyrmhide',
                'Star-Mother','Vital-Unity',
                'Sinister-Deeds','Mystical-Energy',
                'Evocation','Splendor','Sadamune']

        armors = ['Dominion', 'Wyrmhide','Star-Mother']

        weapons = ['Vital-Unity','Sinister-Deeds','Mystical-Energy','Evocation','Splendor','Sadamune']

        dp_guild = self.bot.get_guild(374716378655227914) 
        staff_role = discord.utils.get(dp_guild.roles, name="Staff")
        leader_role = discord.utils.get(dp_guild.roles, name="Leader")
        founder_role = discord.utils.get(dp_guild.roles, name="Founder")
        trial_role = discord.utils.get(dp_guild.roles, name="Trial staff")
        roles = [staff_role, leader_role, founder_role, trial_role]
        staff_users = [i for i in dp_guild.members if any(y in i.roles for y in roles)]
        # for x in dp_guild.members:
        #     if any(y in x.roles for y in roles):
        #         staff_users.append(x)        
        for user in staff_users:
            if not str(user.id) in str(raffle_settings):
                raffle_settings[user.id] = {}
                raffle_settings[user.id]['Name'] = str(user)
                raffle_settings[user.id]['Pot Only'] = False
                raffle_settings[user.id]['Items Only'] = False
                raffle_settings[user.id]['Disabled Pots'] = {}
                raffle_settings[user.id]['Disabled Items'] = {}
                for pot in pots:
                    raffle_settings[user.id]['Disabled Pots'][pot] = False
                for item in items:
                    raffle_settings[user.id]['Disabled Items'][item] = False
                              

        with open("root/Satori/raffle_settings.json", "w+") as fp:
                json.dump(raffle_settings, fp, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        
        with open("root/Satori/logs.json", "r") as f:
            logs = json.load(f)
        if message.guild.id == 374716378655227914:
            await start_logs(self, message)
        if message.channel.id == 412693781540765696:
            user = await self.bot.fetch_user(message.author.id)
            role = discord.utils.get(message.guild.roles, name="applied")
            Member = discord.utils.get(message.guild.roles, name='Member')
            dp_role = discord.utils.get(message.guild.roles, name='Death Poet')
            tzone = ['time zone', 'timezone', 'tz']
            ign = ['ingame name', 'in game name', 'ign']
            char = ['characters', 'character(s)', 'character']
            strx = message.content.lower()
            if 'fame' in strx and any(y in strx for y in tzone) and any(z in strx for z in ign) and any(w in strx for w in char):
                await user.send("Your application has been submitted. Allow up to 24 hours for a response. If there's an issue, please contact a staff member immediately.")
                await message.author.add_roles(role)
                chan = await self.bot.fetch_channel(374720030387994625) 
                components = [ActionRow(Button(label='Accept',
                                    custom_id='yes_button',
                                    style=ButtonStyle.green
                                    ),
                                Button(label='Decline',
                                    custom_id='no_button',
                                    style=ButtonStyle.red))
                    ]
                msg = await chan.send(f"<@&374717311422300182>, a new application from: {str(user)} ({user.id})\n ```{message.content}```", components = components)
                def _check(i: discord.ComponentInteraction, b):
                    return i.message == msg
                admin = discord.utils.get(message.guild.roles, name="Staff")
                leader = discord.utils.get(message.guild.roles, name="Leader")
                Founder = discord.utils.get(message.guild.roles, name="Founder")
                staff_candidate = discord.utils.get(message.guild.roles, name="Trial staff")
                try:
                    while True:
                        interaction, button = await self.bot.wait_for('button_click', check=_check)
                        button_id = button.custom_id
                        await interaction.defer()
                        if staff_candidate or admin or Founder or leader in interaction.author.roles or interaction.author.id == 911306468106571816:
                            if button_id == "yes_button":
                                try:
                                    logs[str(message.guild.id)]['Users'][str(interaction.author.id)]['Accepted'] += 1
                                except Exception as e:
                                    gene = await self.bot.fetch_channel(972473224845729805)
                                    await gene.send(f"ACCEEPTED ERROR {e}")
                                    continue
                            #await interaction.edit(embed=embed, components= [])
                                updated_guild = self.bot.get_guild(374716378655227914)
                                if not user in updated_guild.members:
                                    await interaction.respond("User has left the server.")
                                    return
                                if role in message.author.roles:
                                    await user.send("You're application was approved. You should now have access to text and voice channels.")
                                    await interaction.edit(content=f"<@&374717311422300182>, a new application from: {str(user)} ({user.id})\n ```{message.content}```\n ✅ Approved ✅ by {str(interaction.author)}", components = [])
                                    await interaction.respond("User has been notified that they're application has been approved.", hidden=True, delete_after=5)
                                    try:
                                        await message.author.remove_roles(role)
                                    except Exception as e:
                                        print(e)
                                        await interaction.respond("Error applying role. This is either because User is no longer in the server, or is due to user not having the 'applied' role when you clicked Accept. The member role should still be automatically applied.", hidden=True)
                                        logs[str(message.guild.id)]['Error Applying Role'] += 1
                                    else:
                                        logs[str(message.guild.id)]['Accepted Applications'] += 1
                                    finally:
                                        await message.author.add_roles(dp_role)
                                        with open("root/Satori/logs.json", "w+") as fp:
                                            json.dump(logs, fp, indent=4)
                                    return
                            elif button_id == 'no_button': #Pressed Decline button
                                try:
                                    logs[str(message.guild.id)]['Users'][f'{interaction.author.id}']['Declined'] += 1
                                except Exception as e:
                                    gene = await self.bot.fetch_channel(972473224845729805)
                                    await gene.send(f"DECLINED ERROR : {e}")
                                    continue
                                application_buttons = [ActionRow(Button(label='Under Reqs',
                                    custom_id='reqs',
                                    style=ButtonStyle.green),
                                Button(label='Custom Reason',
                                    custom_id='custom',
                                    style=ButtonStyle.green),
                                Button(label='None',
                                    custom_id='none',
                                    style=ButtonStyle.green)
                                    )
                                    ]
                                updated_guild = self.bot.get_guild(374716378655227914)
                                if not user in updated_guild.members:
                                    await interaction.respond("User has left the server.")
                                    return
                                await interaction.edit(content=f"<@&374717311422300182>, a new application from: {user.name}#{user.discriminator} ({user.id})\n ```{message.content}```\n🚫 Denied 🚫 by {interaction.author.name}#{interaction.author.discriminator}", components = [])
                                dong = await interaction.respond("Reason?", hidden=True, components = application_buttons, delete_after=120)
                                logs[str(message.guild.id)]['Declined Applications'] += 1
                                with open("root/Satori/logs.json", "w+") as fp:
                                    json.dump(logs, fp, indent=4)
                                def check(m: discord.ComponentInteraction, but):
                                    return m.author == interaction.author
                                try:                            
                                    i, b = await self.bot.wait_for('button_click', check=check, timeout = 120.0)
                                    await i.defer()
                                except asyncio.TimeoutError:
                                    await user.send("Your application was denied.")
                                    await dong.edit(content='Interaction timed out. User has been notified. ',components = [],delete_after=8)
                                if b.custom_id == "reqs":
                                    await interaction.edit(
                                        content=f"<@&374717311422300182>, a new application from: {user.name}#{user.discriminator} ({user.id})\n ```{message.content}```\n🚫 Denied 🚫 by {interaction.author.name}#{interaction.author.discriminator} for `Not meeting requirements.`", components = [])
                                    await user.send("Your application was denied for: `Under requirements.`.")
                                    await dong.edit(content='User has been notified.',components = [], delete_after=8)
                                elif b.custom_id == "custom":
                                    await dong.edit(content="Type your reason.", components = [])
                                    def reason_check(e):
                                        return e.author == i.author and e.channel == i.channel
                                    try:                            
                                        reason = await self.bot.wait_for('message', check=reason_check, timeout = 60.0)
                                    except asyncio.TimeoutError:
                                        await i.respond("Timed out. Sent no reason.", hidden=True,)
                                        await dong.edit(content='User has been notified.',components = [], delete_after=8) 
                                    else:
                                        await user.send(f"Your application was denied for the following reason:\n```{reason.content}``` ")
                                        await interaction.edit(
                                            content=f"<@&374717311422300182>, a new application from: {user.name}#{user.discriminator} ({user.id})\n ```{message.content}```\n🚫 Denied 🚫 by {interaction.author.name}#{interaction.author.discriminator} for `{reason.content}`", components = [])
                                        await reason.delete()
                                        await dong.edit(content=f'User has been notified for `{reason.content}`',components = [], delete_after=8)
                                elif b.custom_id == "none":
                                    await interaction.edit(
                                        content=f"<@&374717311422300182>, a new application from: {user.name}#{user.discriminator} ({user.id})\n ```{message.content}```\n🚫 Denied 🚫 by {interaction.author.name}#{interaction.author.discriminator} with no given reason", components = [])
                                    await user.send('Your application was declined.')
                                    await dong.edit(content='User has been notified.',components = [], delete_after=8)
                                await user.send('Although you have not been accepted, you have been granted the member role so you can still play with us.')
                                await message.author.add_roles(Member)
                                await message.author.remove_roles(role)
                        else:
                            await interaction.respond("You do not have permission to press this button.", hidden=True, delete_after=5)
                except asyncio.TimeoutError:
                    await chan.send("Error due to Timeout. This shouldn't be an issue if it does please DM Mik#1111")
                    return
            else:
                await user.send(f"Your application was deleted due to invalid application format. Here's the application you sent.\n ```{message.content}```")
                await user.send("Copy and paste the following application template.\n**In Game Name and Living fame:**\n**Character(s):**(?/8 [Char. Class], ?/8 [Char. Class], ?/8 [Char. Class] etc.)\n**Time zone:**\n**How you found this Discord:**\n**Comments, Questions, Concerns:**")
                await message.delete()
        elif message.guild.id == 374716378655227914:   
            member = discord.utils.get(message.guild.roles, name="Member")
            applied = discord.utils.get(message.guild.roles, name="applied")
            if member in message.author.roles:
                try:
                    await message.author.remove_roles(applied)
                except Exception as e:
                    gene = await self.bot.fetch_channel(972473224845729805)
                    await gene.send(f"Error removing role called 'applied': {e}")
    @tasks.loop(hours=1)
    async def realmblog_loop(self):
        blog = BlogApi()
        post=0
        r = random.randint(0, 0xffffff)
        content = await blog.content(post)
        content = re.sub('([A-Z])', r' \1', content)
        title, url, date = await blog.title(thread=post), await blog.url(thread=post), await blog.date(thread=post)
        images = await blog.images(thread=post)
        with open("root/Satori/latest.json", "r") as f:
            latest = json.load(f)
        try:
            if not latest['channel']:
                print("Channel not set")
                return
        except:
            print("No channel set <>!")
            return
        channel = str(latest['channel'])
        rchannel = await self.bot.fetch_channel(channel)
        if not "post" in latest:
            latest['post'] = ""
        if not content in latest['post']:
            latest["post"] = content
            #get 2000 characters in the post
            if len(content) > 1995:
                content = content[:1995] + "[...]"
            else:
                content = content + "[...]"
            embed = discord.Embed(title=f"{title}", description=f"{content}", color=r)
            embed.set_author(name=f"Click here to view the rest of the post!", url=f"{url}", icon_url="https://remaster.realmofthemadgod.com/favicon.png")
            embed.set_footer(text=f"Date posted: {date}")
            try:
                embed.set_image(url=images[0])
            except:
                pass
            await rchannel.send(embed=embed)
            with open("root/Satori/latest.json", "w") as f:
                json.dump(latest, f, indent=4)

    
    @commands.is_owner()
    @commands.Cog.slash_command(
        name='realmblog', 
        description='Gets post from remaster.realmofthemadgod.com',
        options=[
            Option(
                option_type=int,
                name='index',
                description='Index of post. (0 for the latest, 1 for the next, etc)')
        ],
        guild_ids=[374716378655227914, 972473224845729802])
    async def Blog_Poster(self, ctx: APPCI, index: int=0):
        '''Provides an argument for realmblog.'''
        blog = BlogApi()
        i = 0
        r = random.randint(0, 0xffffff)
        content = await blog.content(index)
        content = re.sub('([A-Z])', r' \1', content)
        title, url, date = await blog.title(thread=index), await blog.url(thread=index), await blog.date(thread=index)
        images = await blog.images(thread=index)
        #get 2000 characters in the post
        if len(content) > 1995:
            content = content[:1995] + "[...]"
        else:
            content = content + "[...]"
        embed = discord.Embed(title=f"{title}", description=f"{content}", color=r)
        embed.set_author(name=f"Click here to view the rest of the post!", url=f"{url}", icon_url="https://remaster.realmofthemadgod.com/favicon.png")
        embed.set_footer(text=f"Date posted: {date}")
        try:
            embed.set_image(url=images[0])
        except:
            pass
        await ctx.channel.send(embed=embed)
        #await realmblog(int)

    @commands.Cog.slash_command(
        name='appinfo',
        description='Information for mods and applications'
    )
    async def modinfo(self, ctx : APPCI):
        with open("root/Satori/logs.json", "r") as f:
            logs = json.load(f)
        datetime_str = '10/1/2022 12:00'

        datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')

        # log_start_time = datetime.strptime(dt_str, '%m/%d/%y')
        embed = discord.Embed(title=f"Application info.", description=f'Due to corruption, started individual logging {discord.utils.styled_timestamp(datetime_object, "D")}.', color=random.randint(0,0xffffff))
        # for c in logs[str(ctx.guild.id)]['Users']:
        #     ids.append(c)
        ids = [c for c in logs[str(ctx.guild.id)['Users']]]

        for id in ids:
            if id in logs[str(ctx.guild.id)]['Users']:
                accepted = logs[str(ctx.guild.id)]['Users'][str(id)]['Accepted']
                declned = logs[str(ctx.guild.id)]['Users'][str(id)]['Declined']
                user = await self.bot.fetch_user(id)
                embed.add_field(name=str(user), value=f'Accepted: `{accepted}`|Declined: `{declned}`', inline=True)
        acp = logs[str(ctx.guild.id)]['Accepted Applications']
        dec = logs[str(ctx.guild.id)]['Declined Applications']
        embed.set_footer(text=f'Total amount of applications submitted since 9/2/22: {acp + dec}')
        await ctx.respond(embed=embed)

#####RAFFLE MODULE#####

    @commands.Cog.slash_command(
        base_name='raffle',
        base_desc='Start a new raffle.',
        name='start',
        description='Starts a raffle, and sends an embed that edits itself when items are submitted.',
        guild_ids=[374716378655227914, 972473224845729802],
        default_required_permissions=Permissions(manage_messages=True))
    async def raffle_msg(self, ctx: APPCI):
        logging.basicConfig(filename='root/Satori/logs/raffle_logs.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        components = [ActionRow(
            Button(label='Submit',
            custom_id='raffle_submit',
            style=ButtonStyle.green),
            Button(label='Edit',
            custom_id='raffle_edit',
            style=ButtonStyle.gray),
            Button(label='Delete',
            custom_id='raffle_del',
            style=ButtonStyle.red))
        ]
        global yn_comps
        yn_comps=[ActionRow(
                    Button(
                        label='Yes',
                        custom_id='yes',
                        style=ButtonStyle.green),
                    Button(
                        label='No',
                        custom_id='no',
                        style=ButtonStyle.red))
                        ]
        global quan_components
        quan_components=[ActionRow(), ActionRow()]
        nums = {
            1 : '1️⃣',
            2 : '2️⃣',
            3 : '3️⃣',
            4 : '4️⃣',
            5 : '5️⃣',
            6 : '6️⃣',
            7 : '7️⃣',
            8 : '8️⃣'
        }
        for i in range(1, 9):
            f = nums[i]
            but = Button(
                emoji=f,
                custom_id=f'q|{i}',
                style=ButtonStyle.grey
            )
            if i < 5:
                quan_components[0].add_component(but)
            else:
                quan_components[1].add_component(but)
        global raffle_embed, raffle_author, _msg
        raffle_embed = discord.Embed(
            title=f"Press the button below to submit items into the raffle for a chance to win.", 
            description=f"**How it works**:\n After pressing the button, you'll be asked to select what type of item you want to submit. Afterwards, you'll be asked to enter the quantity of the items. Just type the message into the channel the amount. Once this is done, the staff member who started the raffle will get a notification. They will contact you to trade over the items to them in game. Winners are decided based on probability and how many submissions were entered.",
            color=random.randint(0, 0xffffff))
        raffle_embed.set_author(name=f'New Raffle started by {str(ctx.author)}.')
        raffle_author = ctx.author
        _msg = await ctx.respond(embed=raffle_embed, components=components)
        
        global raffle_started
        raffle_started = True
            

    @commands.Cog.on_click('raffle_submit')
    #person clicks buytton, staff gets notification to confirm if items have been traded
    async def raffle_submit(self, interaction: ComponentInteraction, button):
        global submit_interaction
        submit_interaction = interaction
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        item_settings = settings[str(raffle_author.id)]['Disabled Items']
        p_settings = settings[str(raffle_author.id)]['Disabled Pots']

        original_options = []
        
        for p in pots:
            if not p_settings[p]:
                original_options.append(SelectOption(emoji=emojis['Life'], label='Potions', value='Potions', description='Another menu will let you select which types of pot.'))
                break
        for wep in weapons:
            if not item_settings[wep]:
                original_options.append(SelectOption(emoji=emojis['Vital-Unity'], label='T13 Weapons', value='T13Weapon', description='Ranging from ~4GL to 1 Deca'))
                break
        if not item_settings['Dominion'] or not item_settings['Wyrmhide'] or not item_settings['Star-Mother']:
            original_options.append(SelectOption(emoji=emojis['Dominion'], label='T14 Armors', value='T14Armor', description='Worth ~3GL'))
        if not item_settings['Deca']:
            original_options.append(SelectOption(emoji=emojis['Deca'], label='Ring of Decade', value='Deca', description='Deca rings worth ~16GL'))
        if not item_settings['Ubhp']:
            original_options.append(SelectOption(emoji=emojis['Ubhp'], label='Unbound HP', value='Ubhp', description='Ring of Unbound Health'))
        components = [[SelectMenu(custom_id='_select_', options=original_options,
            placeholder='Select an option', max_values=1)
        ]]

        if settings[str(raffle_author.id)]['Pot Only'] == True and settings[str(raffle_author.id)]['Items Only'] == False:
            components = [[SelectMenu(custom_id='_select_', options=[
            SelectOption(emoji=emojis['Life'], label='Potions', value='Potions',
                        description='Another menu will let you select which types of pot.')
        ],
            placeholder='Raffle author has selected a Pot Only raffle.', max_values=1)
        ]]

        item_ops = []


        if not settings[str(raffle_author.id)]['Pot Only'] and settings[str(raffle_author.id)]['Items Only']:
            if not item_settings['Deca']:
                item_ops.append(SelectOption(emoji=emojis['Deca'], label='Ring of Decade', value='Deca', description='Deca rings worth ~16GL'))
            if not item_settings['Ubhp']:
                item_ops.append(SelectOption(emoji=emojis['Ubhp'], label='Unbound HP', value='Ubhp', description='Ring of Unbound Health'))
            
            
            
            for wep in weapons:
                if not item_settings[wep]:
                    item_ops.append(SelectOption(emoji=emojis[wep], label='T13 Weapons', value='T13Weapon', description='Ranging from ~4GL to 1 Deca'))
                    break
            for arm in armors:
                if not item_settings[arm]:
                    item_ops.append(SelectOption(emoji=emojis[arm], label='T14 Armors', value='T14Armor', description='Worth ~3GL'))
                    break
                
            components = [[SelectMenu(custom_id='_select_', options=item_ops,
            placeholder='Raffle author has selected an Item Only raffle.', max_values=1)
        ]]
        
        rings = ['Ubhp', 'Deca']
        msg_with_selects = await interaction.respond('What items do you want to put into the raffle?', components=components, hidden=True)   
        def check_selection(i: discord.ComponentInteraction, select_menu):
            return i.author == interaction.author and i.channel == interaction.channel and select_menu.custom_id == '_select_'
        try:
            select_interaction, select_menu = await self.bot.wait_for('selection_select', check=check_selection, timeout=15)
        except asyncio.TimeoutError:
            await msg_with_selects.edit(content='Selection timed out.', components=[])
            return
        submission = {}
        await select_interaction.defer()
        await msg_with_selects.edit(content='What items do you want to put into the raffle?', components=[])
        def yes_no_check(i: ComponentInteraction, b):
            return i.author == interaction.author and i.channel == interaction.channel
        def quan_check(i: ComponentInteraction, b):
            return i.author == interaction.author and i.channel == interaction.channel and 'q|' in b.custom_id
        ##########POTS SELECTION##########
        if len(select_menu.values) == 1 and 'Potions' in select_menu.values:
            
            options = [SelectOption(emoji=emojis[pot], label=pot, value=pot, description=f'Potion of {pot}')
                        for pot in pots if not settings[str(raffle_author.id)]['Disabled Pots'][pot]]
            pot_comps = [[SelectMenu(custom_id='potion_select', options=options,
                                    placeholder='Select some pots', max_values=len(options))            ]]


            pot_select_msg = await msg_with_selects.edit(content='Select which pots you want to submit.', components=pot_comps)
            def _check_select(i: ComponentInteraction, potion_select_menu):
                return i.author == interaction.author and i.channel == interaction.channel and potion_select_menu.custom_id == 'potion_select'

            try:
                potion_select_interaction, potion_select_menu = await self.bot.wait_for('selection_select', check=_check_select, timeout=15)
            except asyncio.TimeoutError:
                await pot_select_msg.edit(content='Selection timedout. Try again.', components=[])
                return
            await potion_select_interaction.defer()
            await pot_select_msg.edit(content='Select which pots you want to submit.', components=[])
            
            ######SELECTED MULITPLE POTS######
            if len(potion_select_menu.values) >= 2:
                pots_quan = []
                for index, value in enumerate(potion_select_menu.values):
                    if index == 0:
                        enter = await pot_select_msg.edit(content=f'How many {emojis[value]} pots do you want to submit?', components=quan_components)
                    elif index > 0:
                        await enter.edit(content=f'{enter.content}\nHow many {emojis[value]} pots do you want to submit?', components=quan_components)
                    try:
                        pts_q_int, pts_button = await self.bot.wait_for('button_click', check=quan_check, timeout=10)
                    except asyncio.TimeoutError:
                        await enter.edit(content='Quantity submission has been timed out. Cancelling...', components=[])
                        return
                    pot_quan = pts_button.custom_id[2:]
                    await pts_q_int.defer()
                    await enter.edit(content=f"{enter.content}\nEntered {pot_quan} {emojis[value]} pots.", components=[])
                    pots_quan.append(pot_quan)

                submission = {key: value for key, value in zip(potion_select_menu.values, pots_quan)}



                await raffle_submission(self, interaction=interaction, submission=submission, message=enter)
                await enter.edit(content='Your pots have been submitted successfully.', components=[])
              
            #######SELECTED ONE POT ONLY##########
            elif len(potion_select_menu.values) == 1:
                await pot_select_msg.edit(content=f"How many {potion_select_menu.values[0]} pots do you want to submit?", components=quan_components)
                try:
                    quantity_int, quantity_button = await self.bot.wait_for('button_click', check=quan_check, timeout=10)
                except asyncio.TimeoutError:
                    await pot_select_msg.edit(content='Quantity submission has been timed out. Cancelling...')
                    return
                else:
                    await quantity_int.defer()
                    pot_quantity = quantity_button.custom_id[2:]
                await pot_select_msg.edit(content=f"Are you sure you want to submit {pot_quantity} {potion_select_menu.values[0]} pots?", components=yn_comps)
                try:
                    yes_no_interaction, yes_no_button = await self.bot.wait_for('button_click', check=yes_no_check, timeout=10)
                except asyncio.TimeoutError:
                    await pot_select_msg.edit(content="Item not submitted by timeout.", components = [])
                    return
                await yes_no_interaction.defer()
                yn_button_id = yes_no_button.custom_id
                if yn_button_id == 'yes':
                    submission[f'{potion_select_menu.values[0]}'] = pot_quantity
                    await pot_select_msg.edit(content='Your item has been submitted.', components=[])
                else:
                    await pot_select_msg.edit(content="Item not submitted.", components = [])
                    return 
                await raffle_submission(self, interaction=interaction, submission=submission, message=pot_select_msg)

        ##########RING SELECTION##########
        elif any(y in select_menu.values for y in rings):
            ring_type = select_menu.values[0]
            ring_emoji = None
            if ring_type == 'Deca':
                ring_emoji = emojis['Deca']
            elif ring_type == 'Ubhp':
                ring_emoji = emojis['Ubhp']
            submit_msg = await msg_with_selects.edit(content=f'How many {ring_emoji} rings do you want to submit?', components=quan_components)
            def quan_check(i: ComponentInteraction, b):
                return i.author == interaction.author and i.channel == interaction.channel and 'q|' in b.custom_id
            try:
                quantity_interaction, quantity_button = await self.bot.wait_for('button_click', check=quan_check, timeout=10)
            except asyncio.TimeoutError:
                await submit_msg.edit(content='Quantity submission timed out.',components=[])
                return
            else:
                await quantity_interaction.defer()
                ring_quantity = quantity_button.custom_id[2:]
                await submit_msg.edit(content=f'You\'ve successfully submitted {ring_quantity}x{ring_emoji}!', components=[])
                submission[ring_type] = ring_quantity
                await raffle_submission(self, interaction=interaction, submission=submission, message=submit_msg)
        #########ARMOR SELECTION##########
        elif 'T14Armor' in select_menu.values:
            arm_ops = []
            for arm in armors:
                if item_settings[arm] == False:
                    arm_description = descriptions.get(arm, "")
                    arm_ops.append(SelectOption(emoji=emojis[arm], label=arm, value=arm, description=arm_description))
            armor_components = [[SelectMenu(custom_id='armor_select', options=arm_ops,
                                    placeholder='Select armor to submit', max_values=1)
                                ]]
            global armor_msg
            armor_msg = await msg_with_selects.edit(content='What items do you want to put into the raffle?', components=armor_components)   

        ##########WEAP SELECT#############
        elif 'T13Weapon' in select_menu.values:

            wep_ops = []
            for wep in weapons:
                if not item_settings[wep]:
                    wep_description = descriptions.get(wep, "")
                    wep_ops.append(SelectOption(emoji=emojis[wep], label=wep, value=wep, description=wep_description))
            weapon_components = [[SelectMenu(custom_id='weapon_select', options=wep_ops,
                                    placeholder='Select a weapon to submit', max_values=1)
                                    ]]

            # wep_ops = [SelectOption(emoji=emojis[wep], label=wep, value=wep, description=descriptions.get(wep, ""))
            #             for wep in weapons if item_settings[wep] == False]
            #weapon_components = [[SelectMenu(custom_id='weapon_select', options=wep_ops,
            #                      placeholder='Select a weapon to submit', max_values=1)]]
            
            global weapon_msg
            weapon_msg = await msg_with_selects.edit(content='Select which type of weapons you want to submit:', components=weapon_components)


    @commands.Cog.on_select(custom_id='weapon_select')
    async def on_weapon_sel(self, interaction, select_menu):
        submission = {}
        await interaction.defer()
        #await weapon_msg.edit(content=f'How many {select_menu.values[0]} do you want to submit?', components=[])
        quantity_button_msg = await weapon_msg.edit(content=f'How many {select_menu.values[0]} do you want to submit?', components=quan_components)
        weapon_type = select_menu.values[0]
        weapon_emoji = emojis[weapon_type]
        if not submission:
            def quan_check(i: ComponentInteraction, b):
                return i.author == interaction.author and i.channel == interaction.channel and 'q|' in b.custom_id
            try:
                quantity_interaction, quantity_button = await self.bot.wait_for('button_click', check=quan_check, timeout=10)
            except asyncio.TimeoutError:
                await quantity_button_msg.edit(content='Quantity submission timed out.',components=[])
                return
            else:
                await quantity_interaction.defer()
                weapon_quantity = quantity_button.custom_id[2:]
                await quantity_button_msg.edit(content=f'You\'ve successfully submitted {weapon_quantity}x{weapon_emoji}!', components = [])
                submission[weapon_type] = weapon_quantity
                await raffle_submission(self, interaction=interaction, submission=submission, message=quantity_button_msg)
                     
    @commands.Cog.on_select(custom_id='armor_select')
    async def on_armor_sel(self, interaction, select_menu):
        submission = {}
        await interaction.defer()
        #await armor_msg.edit(content=f'How many {select_menu.values[0]} do you want to submit?', components=[])
        quantity_button_msg = await armor_msg.edit(content=f'Click one of the buttons to submit your quantity:', components=quan_components)
        armor_type = select_menu.values[0]
        armor_emoji = emojis[armor_type]
        if not submission:
            def quan_check(i: ComponentInteraction, b):
                return i.author == interaction.author and i.channel == interaction.channel and 'q|' in b.custom_id
            try:
                quantity_interaction, quantity_button = await self.bot.wait_for('button_click', check=quan_check, timeout=10)
            except asyncio.TimeoutError:
                await quantity_button_msg.edit(content='Quantity submission timed out.',components=[])
                return
            else:
                await quantity_interaction.defer()
                armor_quantity = quantity_button.custom_id[2:]
                await quantity_button_msg.edit(content=f'You\'ve successfully submitted {armor_quantity}x{armor_emoji}!', components = [])
                submission[armor_type] = armor_quantity
                await raffle_submission(self, interaction=interaction, submission=submission, message=quantity_button_msg)
        
    @commands.Cog.on_click('raffle_edit')
    async def raffle_edit(self, interaction: ComponentInteraction, b):
        b_name, components, embed_dict = None, [ActionRow()], raffle_embed.to_dict()
        # components = [ActionRow()]
        # embed_dict = raffle_embed.to_dict()
        if interaction.author == raffle_author:
            if len(raffle_embed.fields) > 0:
                name_comps, usernames = [ActionRow()], []
                for proxy in raffle_embed.fields:
                    name_submissions = proxy.name
                    if not name_submissions == interaction.author:
                        usernames.append(name_submissions)   
                # if str(interaction.author) in usernames:
                #     usernames.remove(str(interaction.author))
                for x in usernames:
                    button = Button(label=f'{x}', custom_id=f'name#{x}', style=ButtonStyle.blurple)
                    name_comps[0].add_component(button)
                user_msg = await interaction.respond(f"Which user's submissions do you want to edit?",components=name_comps,hidden=True)
                def check(i,b):
                    return i.author == interaction.author and i.channel == interaction.channel and "name#" in b.custom_id
                try:
                    i, b = await self.bot.wait_for('button_click', check=check, timeout=10)
                except asyncio.TimeoutError:
                    await user_msg.edit(content='Delete cancelled due to timeout.')
                    return
                await i.defer()
                b_name = b.custom_id[5:]
                emb_value = None
                for pxy in raffle_embed.fields:
                    if pxy.name == b_name:
                        emb_value = pxy.value
                        break
                if " " in emb_value:
                    emb_value = emb_value.replace(' ', '')
                emb_list = emb_value.split('\n')
                for x in emb_list:
                    rand_id = random.randint(1000, 9999)
                    em_res = re.sub(r'(x[a-zA-Z0-9\s].*?\b).*$', "", str(x))
                    res = re.sub(r'.+?(?=x)', "", x)
                    button_= Button(label=f'{res}', emoji=f'{em_res}', custom_id=f'--{x}({rand_id})', style=ButtonStyle.blurple)
                    components[0].add_component(button_)
                await user_msg.edit(content="Which submissions do you want to delete?", components=components)
                def del_check(i, b):
                    return i.author == interaction.author and i.channel == interaction.channel and bool(re.search(r'^--[a-zA-Z<>: 0-9()]+$', b.custom_id)) == True
                try:
                    d_int, d_b = await self.bot.wait_for('button_click', check=del_check, timeout=15)
                except asyncio.TimeoutError:
                    await user_msg.edit(content='Delete cancelled due to timeout.')
                    return
                await d_int.defer()
                entry = d_b.custom_id[2:-6]
                await user_msg.edit(content=f'Are you sure you want to remove {entry} from {b_name}\'s submissions?', components=yn_comps)
                def yn_check(i,yn_b):
                    return i.author == interaction.author and yn_b.custom_id in ["no", "yes"]
                try:
                    yn_int, yn_button = await self.bot.wait_for('button_click', check=yn_check, timeout=15)
                except asyncio.TimeoutError:
                    await user_msg.edit(content='Button timed out. Deletion cancelled.', components=[])
                    return
                await yn_int.defer()
                if yn_button.custom_id == 'yes':
                    embed_old_value = None
                    for field in embed_dict['fields']:
                        if field['name'] == b_name:
                            if " " in field['value']:
                                f = str(field['value'])
                                f = f.replace(" ", "")
                                field['value'] = f
                            if entry in field['value']:
                                embed_old_value = str(field['value']).split('\n')
                                if entry in embed_old_value:
                                    embed_old_value.remove(str(entry))
                                    value = '\n'.join(c for c in embed_old_value)
                                    if " " in value:
                                        value = value.replace(" ", "")
                                    field["value"] = value
                                    break
                    if value == "":
                        fields = raffle_embed.fields
                        for index, field in enumerate(fields):
                            if field.name == b_name:
                                raffle_embed.remove_field(index)
                                break
                    e = discord.Embed.from_dict(embed_dict)
                    await user_msg.edit(content=f'You have deleted {entry} from {b_name} submissions.', components=[])
                    await _msg.edit(embed=e)
                else:
                    await user_msg.edit(content='Deletion cancelled.')
                    return
        else:
            await interaction.respond('Only the raffle author can use this.', hidden=True)
            return

    @commands.Cog.on_click('raffle_del')
    async def raffle_delete(self, interaction: ComponentInteraction, button):
        field_value = None
        components = [ActionRow()]
        if not str(interaction.author) in str(raffle_embed.fields):
            await interaction.respond('You do not have any entires.', hidden=True)
            return
        if str(interaction.author) in str(raffle_embed.fields):
            embed_dict = raffle_embed.to_dict()
            for field in embed_dict["fields"]:
                if field["name"] == str(interaction.author):
                    field_value = field["value"]
            field_value = str(field_value).split("\n")
        used_ids = []
        for submission in field_value:
            rand_id = random.randint(1000, 9999)
            if rand_id in used_ids:
                rand_id = random.randint(1000, 9999)
            used_ids.append(rand_id)
            emoji_result = re.sub(r'(x[a-zA-Z0-9\s].*?\b).*$', "", str(submission))
            result = re.sub(r'.+?(?=x)', "", submission)
            if " " in emoji_result:
                emoji_result = emoji_result.replace(" ", "")
            
            button = Button(label=f'{result}', emoji=f'{emoji_result}', custom_id=f'--{submission}({rand_id})', style=ButtonStyle.blurple)
            components[0].add_component(button)
        msg = await interaction.respond(f"What entry do you want to delete?", hidden=True, components=components)
        def del_check(i, b):
            return i.author == interaction.author and i.channel == interaction.channel and bool(re.search(r'^--[a-zA-Z<>: 0-9()]+$', b.custom_id)) == True
        try:
            b_inter, b_button = await self.bot.wait_for('button_click', check=del_check, timeout=10)
        except asyncio.TimeoutError:
            await msg.edit(content='Button timed out.', components=[])
            return
        await b_inter.defer()
        entry = b_button.custom_id[2:-6]
        await msg.edit(content=f'Are you sure you want to remove {entry} from your submissions?', components=yn_comps)
        def yn_check(i,yn_b):
            return i.author == interaction.author and yn_b.custom_id in ["no", "yes"]
        try:
            yn_int, yn_button = await self.bot.wait_for('button_click', check=yn_check, timeout=10)
        except asyncio.TimeoutError:
            await msg.edit(content='Button timed out. Deletion cancelled.', components=[])
            return
        await yn_int.defer()
        if yn_button.custom_id == 'yes':
            embed_old_value = None
            for field in embed_dict['fields']:
                if field['name'] == str(interaction.author) and entry in field['value']:
#                    if entry in field['value']:
                    embed_old_value = str(field['value']).split('\n')
                    if entry in embed_old_value:
                        embed_old_value.remove(str(entry))
                        value = '\n'.join(c for c in embed_old_value)
                        if " " in value:
                            value = value.replace(" ", "")
                        field["value"] = f'{value}'
                        break
            if value == "":
                fields = raffle_embed.fields
                for index, field in enumerate(fields):
                    if field.name == str(interaction.author):
                        raffle_embed.remove_field(index)
                        break
            e = discord.Embed.from_dict(embed_dict)
            await msg.edit(content=f'You have deleted {entry}', components=[])
            await _msg.edit(embed=e)
        else:
            await msg.edit(content='Deletion cancelled.', components=[])
            return
    
    @commands.Cog.on_click('raffle_win')
    async def raffle_win(self, interaction, button):
        logging.info(f'raffle_win called!')
        await _msg.edit(embed=raffle_embed, components=[])
        embed_dict = raffle_embed.to_dict()
        #players = [field['name'] for field in embed_dict['fields']]
        players, submits, users = [], [], {}
        total_submissions = 0
        for field in embed_dict['fields']:
            player_submits = 0
            val = field['value']
            players.append(field['name'])
            player_submissions = re.sub('.+?(?=x)', '', val)
            player_submissions_list = player_submissions.split('\n')
            for s in player_submissions_list:
                s = s[2:]
                submits.append(int(s))
                total_submissions += int(s)
                player_submits += int(s)
            users[field['name']] = {}
            users[field['name']]['value'] = field['value']
            users[field['name']]['player_submissions'] = player_submits
            if any(p in str(val) for p in pots): 
                pot_list = []
                if "\n" in val:
                    val_list = val.split('\n')
                else:
                    val_list = [val]
                for i in val_list:
                    if any(p in i for p in pots):
                        get_pot_amnt = re.sub('.+?(?=x)', '', i)
                        pot_amnt = get_pot_amnt[2:]
                        pot_list.append(int(pot_amnt))                  
                users[field['name']['total_pots']] = sum(pot_list)
        logging.info(f'Total_submissions = {total_submissions}')

        total_outcomes = sum(submits)
        probabilities = [users[str(player)]['player_submissions']/total_outcomes for player in players]
        logging.info(f'Undistributed probabilities: {probabilities}')

        def distribute_remaining(probs):
            total = sum(probs)
            if total != 1:
                remaining = 1 - total
                probs = [p + (remaining / len(probs)) for p in probs]
            return probs

        distributed_probabilities = distribute_remaining(probabilities)
             
        logging.info(f'information:\n {list(zip(players, distributed_probabilities))}')

        winner = None
        try:
            winner = np.random.choice(players, p=distributed_probabilities)
            logging.info(f'Winner chosen via probability: {winner}')
        except:      
            winner = random.choice(players)
            logging.info(f'Winner chosen via random choosing: {winner}')

        guild_mems = interaction.guild.members
        for user in guild_mems:
            if winner == str(user):
                user_id = user.id

        await interaction.respond(f'Congratulations <@{user_id}>, you have won the raffle! Contact {raffle_author} to claim your items.')


    @commands.Cog.slash_command(
        base_name='raffle',
        base_desc='Raffle close and winner.',
        name='close',
        description='Closes the raffle and choose winner.',
        default_required_permissions=Permissions(manage_messages=True),
        guild_ids=[374716378655227914, 972473224845729802]
        )
    async def raffle_close(self, ctx: APPCI):
        global raffle_started
        if not raffle_started:
            raffle_started = False
        if ctx.author == raffle_author:
            if raffle_started == True:
                raffle_started = False
                await ctx.defer()
                close_comp = [Button(label='Choose Winner',
                                custom_id='raffle_win',
                                style=ButtonStyle.green)]
                await _msg.edit(embed=raffle_embed, components=close_comp)
                await ctx.respond('Successfully closed submissions.', hidden=True)
            else:
                await ctx.respond("No raffle found.", hidden=True)
                return
        else:
            await ctx.respond("Only the raffle author can press this button.", hidden=True)
            return

    '''I think the staffer who's creating the raffle should be able to restrict potions. 
    Say an event is going on that makes attack easy to come by. 
    If he wants to make attack potions a banned item for the raffle it would be nice if he could.'''
    @commands.Cog.slash_command(
        base_name='raffle',
        base_desc='Raffle settings and set up.',
        name='settings',
        description='Configure raffle settings to run it the way you want.',
        default_required_permissions=Permissions(manage_messages=True),
        guild_ids=[374716378655227914, 972473224845729802])
    async def raffle_settings(self, ctx: APPCI):
        global raffle_settings_embed, setting_msg, setting_comps
        setting_comps = [ActionRow(
            Button(label='Pots Only',
            custom_id='setting pot',
            style=ButtonStyle.green),
            Button(label='Items Only',
            custom_id='setting item',
            style=ButtonStyle.green),
            Button(label='Disable Specific Pots',
            custom_id='setting disable_pots',
            style=ButtonStyle.green),
            Button(label='Disable Specific Items',
            custom_id='setting disable_items',
            style=ButtonStyle.green)
        )]
        raffle_settings_embed = discord.Embed(title='Raffle Options', description='')
        raffle_settings_embed.set_author(name=f'{str(ctx.author)}', icon_url=ctx.author.avatar_url)
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        raffle_settings_embed.add_field(name='Pots Only', value=f'{str(bool(settings[str(ctx.author.id)]["Pot Only"]))}', inline=False)
        raffle_settings_embed.add_field(name='Items Only',value=f'{str(bool(settings[str(ctx.author.id)]["Items Only"]))}', inline=False)

        enabled_pots = [emojis[pot] for pot in pots if settings[str(ctx.author.id)]['Disabled Pots'][pot]]
        tes = ' '.join(enabled_pots) if enabled_pots else []

        enabled_items = [emojis[item] for item in items if settings[str(ctx.author.id)]['Disabled Items'][item]]
        tez = ' '.join(enabled_items) if enabled_items else []

    
        raffle_settings_embed.add_field(name='Disabled Pots', value=f'{tes}', inline=False)
        raffle_settings_embed.add_field(name='Disabled Items', value=f'{tez}', inline=False)
        setting_msg = await ctx.respond(embed=raffle_settings_embed, components=setting_comps, hidden=True)

    @commands.Cog.on_click('setting pot')
    async def settings_pot_only(self, interaction, button):
        global setting_msg
        await interaction.defer()
        setting_dict = raffle_settings_embed.to_dict()
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        pot_only = settings[str(interaction.author.id)]['Pot Only']

        item_only = settings[str(interaction.author.id)]['Items Only']

        if pot_only:
            pot_only = False
        else:
            item_only = False
            pot_only = True

        for field in setting_dict['fields']:
            if field['name'] == 'Pots Only':
                field['value'] = str(pot_only)
            if field['name'] == 'Items Only':
                field['value'] = str(item_only)
        settings[str(interaction.author.id)]['Items Only'] = item_only
        settings[str(interaction.author.id)]['Pot Only'] = pot_only
        e = discord.Embed.from_dict(setting_dict)
        await setting_msg.edit(embed=e, components=setting_comps)
        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)

    @commands.Cog.on_click('setting item')
    async def settings_item_only(self, interaction, button):
        global setting_msg
        await interaction.defer()
        setting_dict = raffle_settings_embed.to_dict()
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        item_only = settings[str(interaction.author.id)]['Items Only']
        pot_only = settings[str(interaction.author.id)]['Pot Only']

        if item_only:
            item_only = False
        else:
            pot_only = False
            item_only = True

        for field in setting_dict['fields']:
            if field['name'] == 'Items Only':
                field['value'] = str(item_only)
            if field['name'] == 'Pots Only':
                field['value'] = str(pot_only)

        settings[str(interaction.author.id)]['Items Only'] = item_only
        settings[str(interaction.author.id)]['Pot Only'] = pot_only
        e = discord.Embed.from_dict(setting_dict)
        await setting_msg.edit(embed=e, components=setting_comps)
        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)


    @commands.Cog.on_click('setting disable_pots')
    async def settings_disable_pots(self, interaction, button):        
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        pot_components = [ActionRow(), ActionRow()]
        pot_val = settings[str(interaction.author.id)]['Disabled Pots']
        for i, pot in enumerate(pots):
            f = emojis[pot]
            but = Button(
                emoji=f,
                custom_id=f'pot|{pot}',
                style=ButtonStyle.red if pot_val[pot] else ButtonStyle.green)
            if i < 4:
                pot_components[0].add_component(but)
            else:
                pot_components[1].add_component(but)
        component_msg = await interaction.respond('Which pot do you want to disable?', components=pot_components, hidden=True)
        def check(i,b):
            return i.author == interaction.author and i.channel == interaction.channel and 'pot|' in b.custom_id
        try:
            pot_select_interaction, pot_button = await self.bot.wait_for('button_click', check=check, timeout=15)
        except asyncio.TimeoutError:
            await component_msg.edit(content='Cancelled due to timeout.', components=[])
            await setting_msg.edit(components=setting_comps)
            return
        await pot_select_interaction.defer()
        type_of_pot = pot_button.custom_id[4:]
        pot_emoji = pot_button.emoji
        pot_status = settings[str(interaction.author.id)]['Disabled Pots'][type_of_pot]
        pot_status = not pot_status
        settings[str(interaction.author.id)]['Disabled Pots'][type_of_pot] = pot_status
        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)
        content = None
        if pot_status == False:
            content = f'You have enabled {pot_emoji}'
        else:
            content = f'You have disabled {pot_emoji}. Pot can no longer be submitted.'
        setting_embed_dict = raffle_settings_embed.to_dict()
        
        
        for field in setting_embed_dict['fields']:
            if field['name'] == 'Disabled Pots':
                value = field['value']
                value = value.split(" ") if value != '[]' else []
                if str(pot_emoji) in value:
                    value.remove(str(pot_emoji))
                else:
                    value.append(str(pot_emoji))
                field['value'] = ' '.join(value) if value else '[]'

        
        e = discord.Embed.from_dict(setting_embed_dict)
        await component_msg.edit(content=content, components=[])
        await setting_msg.edit(embed=e, components=setting_comps)
    
    @commands.Cog.on_click('setting disable_items')
    async def settings_disable_items(self, interaction, button):
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        item_comps = [ActionRow(), ActionRow(), ActionRow()]
        _items = items.copy()
        item_val = settings[str(interaction.author.id)]['Disabled Items']
        for i, item in enumerate(_items):
            f = emojis[item]
            b = Button(emoji=f,
                custom_id=f'item|{item}',
                style=ButtonStyle.red if item_val[item] else ButtonStyle.green)
            if i < 4:
                item_comps[0].add_component(b)
            elif i < 8:
                item_comps[1].add_component(b)
            else:
                item_comps[2].add_component(b)
        component_msg = await interaction.respond('Which item do you want to disable?', components=item_comps, hidden=True)
        def disable_item_check(i:discord.ComponentInteraction,b):
            return i.author == interaction.author and i.channel == interaction.channel and 'item|' in b.custom_id
        try: 
            item_select_interaction, item_button = await self.bot.wait_for('button_click', check=disable_item_check, timeout=10)
        except asyncio.TimeoutError:
            await component_msg.edit(content='Cancelled due to timeout.', components=[])
            await setting_msg.edit(components=setting_comps)
        await item_select_interaction.defer()
        item_type = item_button.custom_id[5:]
        item_emoji = item_button.emoji
        item_status = settings[str(interaction.author.id)]['Disabled Items'][item_type]
        item_status = not item_status
        settings[str(interaction.author.id)]['Disabled Items'][item_type] = item_status
        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)
        content = None
        if item_status == False:
            content = f'You have enabled {item_emoji}'
        else:
            content = f'You have disabled {item_emoji}. This item can no longer be submitted.'
        setting_embed_dict = raffle_settings_embed.to_dict()

        for field in setting_embed_dict['fields']:
            if field['name'] == 'Disabled Items':
                value = field['value']
                value = value.split(" ") if value != '[]' else []
                if str(item_emoji) in value:
                    value.remove(str(item_emoji))
                else:
                    value.append(str(item_emoji))
                field['value'] = ' '.join(value) if value else '[]'
                
        e = discord.Embed.from_dict(setting_embed_dict)
        await component_msg.edit(content=content, components=[])
        await setting_msg.edit(embed=e, components=setting_comps)

async def raffle_submission(self, interaction, submission, message = None):
    confirm_comps = [ActionRow(
                    Button(custom_id='con|confirm',
                    style=ButtonStyle.green,
                    emoji= '✔️'),
                    Button(custom_id='con|decline',
                    style=ButtonStyle.red, 
                    emoji= '❌')
    )]
    ch = await self.bot.fetch_channel(1000872338973265940)
    def confirm_check(i, b):
        return i.author == raffle_author and i.channel == ch and 'con|' in b.custom_id
    

                                    #1071134900310257766
    
    embed_dict = raffle_embed.to_dict()


    for key, values in list(submission.items()):
        submission[f"{str(emojis[str(key)])}"] = submission.pop(str(key))
    value = "\n".join([f"{k}x {v}" for k, v in submission.items()])  
    if str(interaction.author) in str(raffle_embed.fields): ###if user already has a submission
        submissions_count = 0
        for field in embed_dict['fields']:
            if field["name"] == str(interaction.author):
                submissions_count += len(field["value"].split("\n"))
        if submissions_count > 8:
            await message.edit(content="You have reached the maximum number of submissions (8) for this raffle.")
            return
        for field in embed_dict["fields"]:
            if field["name"] == str(interaction.author):
                field["value"] += f'\n{value}'
        e = discord.Embed.from_dict(embed_dict)
        await _msg.edit(embed=e)
        return
    
    # if interaction.author != raffle_author:
    #     dat_msg = await ch.send(f'New submission from {interaction.author}:\n{submission}', components=confirm_comps)
    #     con_interaction, con_button = await self.bot.wait_for('button_click', check=confirm_check)
    #     button_id = con_button.custom_id
    #     await con_interaction.defer()
    #     if 'confirm' in button_id:
    #         await dat_msg.edit(content=f'~~New submission from {interaction.author}:~~\nCONFIRMED {submission}')
    #     else:
    #         await dat_msg.edit(content=f'~~New submission from {interaction.author}:~~\DENIED {submission}')
    raffle_embed.add_field(name=f'{str(interaction.author)}', value=value)
    await _msg.edit(embed=raffle_embed)
    
async def start_logs(self, message):    #date of log starting 9/2/22
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
def setup(bot):
    bot.add_cog(DeathPoetsCog(bot))
