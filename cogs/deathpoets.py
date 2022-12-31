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



class DeathPoetsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        global emojis
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

    def cog_unload(self):
        self.realmblog_loop.cancel()

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
        global pots
        with open("root/Satori/raffle_settings.json", "r") as f:
            raffle_settings = json.load(f)
        pots = ['Life', 'Mana', 'Att', 'Def', 'Spd', 'Dex', 'Wis', 'Vit']
        dp_guild = self.bot.get_guild(374716378655227914) 
        staff_role = discord.utils.get(dp_guild.roles, name="Staff")
        leader_role = discord.utils.get(dp_guild.roles, name="Leader")
        founder_role = discord.utils.get(dp_guild.roles, name="Founder")
        trial_role = discord.utils.get(dp_guild.roles, name="Trial staff")
        roles = [staff_role, leader_role, founder_role, trial_role]
        staff_users=[]
        for x in dp_guild.members:
            if any(y in x.roles for y in roles):
                staff_users.append(x)        
        for user in staff_users:
            if not str(user.id) in str(raffle_settings):
                raffle_settings[user.id] = {}
                raffle_settings[user.id]['Name'] = str(user)
                raffle_settings[user.id]['Pot Only'] = False
                raffle_settings[user.id]['Disabled'] = {}
                for pot in pots:
                    raffle_settings[user.id]['Disabled'][pot] = False               

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
        i = 0
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
        ])
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
        ids = []
        datetime_str = '10/1/2022 12:00'

        datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')

        # log_start_time = datetime.strptime(dt_str, '%m/%d/%y')
        embed = discord.Embed(title=f"Application info.", description=f'Due to corruption, started individual logging {discord.utils.styled_timestamp(datetime_object, "D")}.', color=random.randint(0,0xffffff))
        for c in logs[str(ctx.guild.id)]['Users']:
            ids.append(c)
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
        name='new',
        description='Starts a raffle, and sends an embed that edits itself when items are submitted.',
        guild_ids=[374716378655227914, 972473224845729802],
        default_required_permissions=Permissions(manage_messages=True))
    async def raffle_msg(self, ctx: APPCI):
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
        pot_only_components = [
            SelectOption(emoji=emojis['Life'], label='Potions', value='Potions',
                        description='Another menu will let you select which types of pot.')]

        components = [[SelectMenu(custom_id='_select_', options=[
            SelectOption(emoji=emojis['Life'], label='Potions', value='Potions', description='Another menu will let you select which types of pot.'),
            SelectOption(emoji=emojis['Deca'], label='Ring of Decade', value='Deca', description='Deca rings worth ~16GL'),
            SelectOption(emoji=emojis['Ubhp'], label='Unbound HP', value='Ubhp', description='UBHP '),
            SelectOption(emoji=emojis['Vital-Unity'], label='T13 Weapons', value='T13Weapon', description='Ranging from ~4GL to 1 Deca'),
            SelectOption(emoji=emojis['Dominion'], label='T14 Armors', value='T14Armor', description='Worth ~3GL')
        ],
            placeholder='Select an option', max_values=1)
        ]]

        if settings[str(raffle_author.id)]['Pot Only'] == True:
            components = [[SelectMenu(custom_id='_select_', options=[
            SelectOption(emoji=emojis['Life'], label='Potions', value='Potions',
                        description='Another menu will let you select which types of pot.')
        ],
            placeholder='Raffle author has selected a Pot Only raffle.', max_values=1)
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
            pot_comps = [[SelectMenu(custom_id='potion_select', options=[
            SelectOption(emoji=emojis['Life'], label='Life', value='Life', description='Potion of Life or Greater Life.'),
            SelectOption(emoji=emojis['Mana'], label='Mana', value='Mana', description='Potion of Mana or Greater Mana.'),
            SelectOption(emoji=emojis['Att'], label='Att', value='Att', description='Potion of Attack or Greater Attack. '),
            SelectOption(emoji=emojis['Spd'], label='Spd', value='Spd', description='Potion of Speed or Greater Speed.'),
            SelectOption(emoji=emojis['Vit'], label='Vit', value='Vit', description='Potion of Vitality or Greater Vitality.'),
            SelectOption(emoji=emojis['Def'], label='Def', value='Def', description='Potion of Defense or Greater Defense.'),
            SelectOption(emoji=emojis['Dex'], label='Dex', value='Dex', description='Potion of Dexterity or Greater Dexterity.'),
            SelectOption(emoji=emojis['Wis'], label='Wis', value='Wis', description='Potion of Wisdom or Greater Wisdom.')
            ],
                placeholder='Select some pots', max_values=4)
            ]]
            #enabled_pots = []
            options = []
            for pot in pots:
                if settings[str(raffle_author.id)]['Disabled'][pot] == False:
                    #enabled_pots.append(emojis[pot])
                    options.append(SelectOption(emoji=emojis[pot], label=pot, value=pot, description=f'Potion of {pot} or Greater {pot}'))
                    pot_comps = [[SelectMenu(custom_id='potion_select', options=options,
                                    placeholder='Select some pots', max_values=4)
                                ]]
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
                i=1
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
                for key in potion_select_menu.values:
                    for value in pots_quan:
                        submission[key] = value
                        pots_quan.remove(value)
                        break
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
            #await select_interaction.respond(f'How many {ring_type} rings do you want to submit? (Type a number)', hidden=True)
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
            armor_components = [[SelectMenu(custom_id='armor_select', options=[
            SelectOption(emoji=emojis['Dominion'], label='Dominion', value='Dominion', description='T14 Heavy Armor'),
            SelectOption(emoji=emojis['Wyrmhide'], label='Wyrmhide', value='Wyrmhide', description='T14 Leather'),
            SelectOption(emoji=emojis['Star-Mother'], label='Star Mother', value='Star-Mother', description='T14 Robe')            
            ],
                placeholder='Select an armor', max_values=1)
            ]]
            global armor_msg
            armor_msg = await msg_with_selects.edit(content='What items do you want to put into the raffle?', components=armor_components)   

        ##########WEAP SELECT#############
        elif 'T13Weapon' in select_menu.values:
            weapon_components = [[SelectMenu(custom_id='weapon_select', options=[
            SelectOption(emoji=emojis['Vital-Unity'], label='Staff of Vital Unity', value='Vital-Unity', description='T13 Staff'),
            SelectOption(emoji=emojis['Splendor'], label='Sword of Splendor', value='Splendor', description='T13 Sword'),
            SelectOption(emoji=emojis['Mystical-Energy'], label='Bow of Mystical Energy', value='Mystical-Energy', description='T13 Bow'),
            SelectOption(emoji=emojis['Sinister-Deeds'], label='Dagger of Sinister Deeds', value='Sinister-Deeds', description='T13 Dagger'),
            SelectOption(emoji=emojis['Evocation'], label='Wand of Evocation', value='Evocation', description='T13 Wand'),
            SelectOption(emoji=emojis['Sadamune'], label='Sadamune', value='Sadamune', description='T13 Katana')
            ],
                placeholder='Select the type of weapon', max_values=1)
            ]]
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
        b_name = None
        components = [ActionRow()]
        embed_dict = raffle_embed.to_dict()
        if interaction.author == raffle_author:
            if len(raffle_embed.fields) > 0:
                name_comps = [ActionRow()]
                usernames = []
                for proxy in raffle_embed.fields:
                    name_submissions = proxy.name
                    usernames.append(name_submissions)   
                if str(interaction.author) in usernames:
                    usernames.remove(str(interaction.author))
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
                    em_res = re.sub(r'(x[a-zA-Z0-9\s].*?\b).*$', "", str(x))
                    res = re.sub(r'.+?(?=x)', "", x)
                    button_= Button(label=f'{res}', emoji=f'{em_res}', custom_id=f'--{x}', style=ButtonStyle.blurple)
                    components[0].add_component(button_)
                await user_msg.edit(content="Which submissions do you want to delete?", components=components)
                def del_check(i, b):
                    return i.author == interaction.author and i.channel == interaction.channel and bool(re.search(r'^--[a-zA-Z<>: 0-9]+$', b.custom_id)) == True
                try:
                    d_int, d_b = await self.bot.wait_for('button_click', check=del_check, timeout=15)
                except asyncio.TimeoutError:
                    await user_msg.edit(content='Delete cancelled due to timeout.')
                    return
                await d_int.defer()
                entry = d_b.custom_id[2:]
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
        for submission in field_value:
            emoji_result = re.sub(r'(x[a-zA-Z0-9\s].*?\b).*$', "", str(submission))
            result = re.sub(r'.+?(?=x)', "", submission)
            if " " in emoji_result:
                emoji_result = emoji_result.replace(" ", "")
            button = Button(label=f'{result}', emoji=f'{emoji_result}', custom_id=f'--{submission}', style=ButtonStyle.blurple)
            components[0].add_component(button)
        msg = await interaction.respond(f"What entry do you want to delete?", hidden=True, components=components)
        def del_check(i, b):
            return i.author == interaction.author and i.channel == interaction.channel and bool(re.search(r'^--[a-zA-Z<>: 0-9]+$', b.custom_id)) == True
        try:
            b_inter, b_button = await self.bot.wait_for('button_click', check=del_check, timeout=10)
        except asyncio.TimeoutError:
            await msg.edit(content='Button timed out.', components=[])
            return
        await b_inter.defer()
        entry = b_button.custom_id[2:]
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
                if field['name'] == str(interaction.author):
                    if entry in field['value']:
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
        embed_dict = raffle_embed.to_dict()
        users = {}
        players = []
        total_submissions = 0
        submits = []
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
            #99users[field['name']]['total_pots'] = [x for x in embed_dict['fields'] if any(c for c in pots) in embed_dict['fields']]
        probabilities = []
        total_outcomes = 0
        for x in range(0, len(submits)):
            total_outcomes = total_outcomes + submits[x]
        for player in players:
            ways_to_win = users[str(player)]['player_submissions']
            probability = ways_to_win/total_outcomes
            probabilities.append(probability)
        print(submits)
        print(players)
        print(probabilities)
        print(users)
        try:
            if sum(probabilities) == float(1):
                winner = np.random.choice(players, p=probabilities)
        except:
            pass
            #winner = random.choice(player)

        await interaction.respond(f'{winner} won!')


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
        global raffle_settings_embed
        global setting_msg
        global setting_comps
        setting_comps = [ActionRow(
            Button(label='Pots Only',
            custom_id='setting pot',
            style=ButtonStyle.green),
            Button(label='Disable Specific Pots',
            custom_id='setting disable',
            style=ButtonStyle.green)
        )]
        raffle_settings_embed = discord.Embed(title='Raffle Options', description='')
        raffle_settings_embed.set_author(name=f'{str(ctx.author)}', icon_url=ctx.author.avatar_url)
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        raffle_settings_embed.add_field(name='Pots Only', value=f'{str(bool(settings[str(ctx.author.id)]["Pot Only"]))}', inline=False)
        enabled_pots = []
        for pot in pots:
            if settings[str(ctx.author.id)]['Disabled'][pot] == True:
                enabled_pots.append(emojis[pot])
            else:
                continue
        tes = ' '.join(enabled_pots)
        if not tes:
            tes = [] 
        raffle_settings_embed.add_field(name='Disabled Pots', value=f'{tes}', inline=False)
        setting_msg = await ctx.respond(embed=raffle_settings_embed, components=setting_comps)

    @commands.Cog.on_click('setting pot')
    async def settings_pot(self, interaction, button):
        settins = [ActionRow(

            Button(label='Pots Only',

            custom_id='setting pot',
            style=ButtonStyle.green),
            Button(label='Disable Specific Pots',
            custom_id='setting disable',
            style=ButtonStyle.green)
        )]
        await interaction.defer()
        setting_dict = raffle_settings_embed.to_dict()
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        pot_only = settings[str(interaction.author.id)]['Pot Only']
        pot_only = not pot_only
        settings[str(interaction.author.id)]['Pot Only'] = pot_only
        for field in setting_dict["fields"]:
            if field['name'] == 'Pots Only':
                field['value'] = str(pot_only)
        e = discord.Embed.from_dict(setting_dict)
        await setting_msg.edit(embed=e, components=settins)
        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)

    @commands.Cog.on_click('setting disable')
    async def settings_disable(self, interaction, button):
        settins = [ActionRow(



            Button(label='Pots Only',

            custom_id='setting pot',
            style=ButtonStyle.green),
            Button(label='Disable Specific Pots',
            custom_id='setting disable',
            style=ButtonStyle.green)
        )]
        setting_comps[0][0].disabled = True
        await setting_msg.edit(components=setting_comps)
        setting_comps[0][0].disabled = False
        with open("root/Satori/raffle_settings.json", "r") as f:
            settings = json.load(f)
        pot_emojis = {
            'Life': '<:life:1033436223261392916>',
            'Mana': '<:mana:1033436224372871339>',
            'Att': '<:att:1033436220417650798>',
            'Spd': '<:spd:1033436225299816558>',
            'Vit': '<:vit:1033436226553905193>',
            'Def': '<:def:1033436221453635594>',
            'Dex': '<:dex:1033436222330249346>',
            'Wis': '<:wis:1033436227896098856>'

        }
        pot_components = [ActionRow(), ActionRow()]
        for i, pot in enumerate(pots):
            f = pot_emojis[pot]
            but = Button(
                emoji=f,
                custom_id=f'pot|{pot}',
                style=ButtonStyle.grey
            )
            if i < 4:
                pot_components[0].add_component(but)
            else:
                pot_components[1].add_component(but)
        component_msg = await interaction.respond('Which pot should be disabled?', components=pot_components, hidden=True)
        print(component_msg)
        def check(i,b):
            return i.author == interaction.author and i.channel == interaction.channel and 'pot|' in b.custom_id
        try:
            pot_select_interaction, pot_button = await self.bot.wait_for('button_click', check=check, timeout=15)
        except asyncio.TimeoutError:
            await component_msg.edit(content='Cancelled due to timeout.', components=[])
            await setting_msg.edit(components=settins)
            return
        await pot_select_interaction.defer()

        type_of_pot = pot_button.custom_id[4:]
        pot_emoji = pot_button.emoji
        pot_status = settings[str(interaction.author.id)]['Disabled'][type_of_pot]
        pot_status = not pot_status
        settings[str(interaction.author.id)]['Disabled'][type_of_pot] = pot_status
        content = None
        if pot_status == False:
            content = f'You have enabled {pot_emoji}'
        else:
            content = f'You have disabled {pot_emoji}' 
        await component_msg.edit(content=content, components=[])
        setting_embed_dict = raffle_settings_embed.to_dict()
        for field in setting_embed_dict['fields']:
            if field['name'] == 'Disabled':
                if '[]' in field['value']:
                    field['value'] = str(pot_emoji)
                else:
                    if str(pot_emoji) in field['value']:
                        value = field['value']
                        try:
                            value = value.split(" ")
                        except:
                            value = "[]"
                        if isinstance(value, list):
                            value.remove(str(pot_emoji))
                            if len(value) > 1:
                                value = " ".join(value)
                            elif len(value) == 1:
                                value = value[0]
                            elif len(value) == 0:
                                value = '[]'
                        field['value'] = value
                    else:
                        field['value'] += f' {str(pot_emoji)}'

        with open("root/Satori/raffle_settings.json", "w+") as fp:
            json.dump(settings, fp, indent=4)
        e = discord.Embed.from_dict(setting_embed_dict)
        await setting_msg.edit(embed=e, components=setting_comps)

async def raffle_submission(self, interaction, submission, message = None):
    for key, values in list(submission.items()):
        submission[f"{str(emojis[str(key)])}"] = submission.pop(str(key))
    value = "\n".join([f"{k}x {v}" for k, v in submission.items()])  
    if str(interaction.author) in str(raffle_embed.fields): 
        embed_dict = raffle_embed.to_dict()
        var = None
        for field in embed_dict["fields"]:
            if field["name"] == str(interaction.author):
                field["value"] += f'\n{value}'
                var = field['value']
        submissions = var.split('\n')
        if len(submissions) > 8:
            await message.edit(content="You have reached the maximum amount of items in this raffle. (8 submissions)")
            return
        e = discord.Embed.from_dict(embed_dict)
        await _msg.edit(embed=e)
        if interaction.author != raffle_author:
            submissions = "\n".join(submissions)
            await raffle_author.send(f'New submission from {str(interaction.author)}.\n{submissions}')
        return
    raffle_embed.add_field(name=f'{str(interaction.author)}', value=value)
    await _msg.edit(embed=raffle_embed)
    if interaction.author != raffle_author:
        await raffle_author.send(f'New submission from {str(interaction.author)}.\n{value}')


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
