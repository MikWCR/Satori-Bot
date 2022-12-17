import discord
import json
from discord.ext import commands
from discord import SlashCommandOption as Option, Localizations, Permissions, ApplicationCommandInteraction as APPCI
from discord import ActionRow, Button, ButtonStyle
from api.rotmgblog import BlogApi
import random
import re
from datetime import datetime
import asyncio


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
      global start_time
      start_time = datetime.utcnow()
      with open("root/Satori/logs.json", "r") as f:
          logs = json.load(f)
      guild = self.bot.get_guild(374716378655227914) 
      staff_role = discord.utils.get(guild.roles, name="Staff")
      leader_role = discord.utils.get(guild.roles, name="Leader")
      founder_role = discord.utils.get(guild.roles, name="Founder")
      staff_candidate = discord.utils.get(guild.roles, name="Trial staff")
      roles = [staff_role, leader_role, founder_role, staff_candidate]
      guild_users=[]
      for x in guild.members:
        if any(y in x.roles for y in roles):
            guild_users.append(x)
      a=[]
      for user in guild_users:
        if not str(user.id) in str(logs):
            logs[str(guild.id)]['Users'][user.id] = {}
            logs[str(guild.id)]['Users'][user.id]['Name'] = user.name
            logs[str(guild.id)]['Users'][user.id]['Accepted'] = 0
            logs[str(guild.id)]['Users'][user.id]['Declined'] = 0  
            a.append(user)
      with open("root/Satori/logs.json", "w") as fp:
        json.dump(logs, fp, indent=4)
    
    @commands.is_owner()
    @commands.Cog.slash_command(
      name='load',
      description='Loads given cog. File name only.',
      options=[
        Option(
          option_type=str,
          name='cog',
          description='File name')],
      guild_ids=[972473224845729802, 374716378655227914])
    async def load_cog(self, ctx: APPCI, cog: str = None):
        if ctx.author.id ==911306468106571816:
            final_cog = "cogs." + cog
            try:
                self.bot.load_extension(final_cog)
            except Exception as e:
                await ctx.respond(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.respond('**`SUCCESS`**')
      
    @commands.is_owner()
    @commands.Cog.slash_command(
        name='unload',
        description='Unloads given Cog.',
        options=[
            Option(
                option_type = str,
                name = 'cog',
                description= 'File name')
        ],
        guild_ids=[972473224845729802, 374716378655227914]
    )
    async def unload_cog(self, ctx: APPCI, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if ctx.author.id == 911306468106571816:
            final_cog = "cogs." + cog
            print(final_cog)
            try:
                self.bot.unload_extension(final_cog)
            except Exception as e:
                await ctx.respond(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.respond('**`SUCCESS`**')

    @commands.Cog.slash_command(
        name='reload',
        description='Reloads given cog.',
        options=[
            Option(
                option_type=str,
                name='cog',
                description='File name')
        ],
        guild_ids=[972473224845729802,374716378655227914]
    )
    @commands.is_owner()
    async def dcog_reload(self, ctx: APPCI, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if ctx.author.id == 911306468106571816:
            final_cog = "cogs." + cog
            try:
                self.bot.unload_extension(final_cog)
                self.bot.load_extension(final_cog)
            except Exception as e:
                await ctx.respond(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.respond('**`SUCCESS`**')


   
    @commands.is_owner()
    @commands.Cog.slash_command(
      name='restart',
      description='Restarts Satori.',
      guild_ids=[972473224845729802, 374716378655227914])
    async def restart(self, ctx: APPCI):
      if ctx.author.id == 911306468106571816:
        await ctx.respond(f":wave: `{self.bot.user.name}` is restarting...") # type: ignore
        await self.bot.close()
    
    @commands.Cog.slash_command(
      name='uptime',
      description='Shows how long Satori has been online.')
    async def uptime(self, ctx):
      uptime = datetime.utcnow()-start_time
      await ctx.respond(f'Uptime: {uptime}')
    
    @commands.is_owner()
    @commands.Cog.slash_command(
        name='addbal',
        description='Owner Only for Debugging. Adds money to balance.',
        options=[
            Option(
                option_type=int,
                name='amount',
                description='The amount of munnies to be added.',
                required=True
            ),
            Option(
                option_type=discord.Member,
                name='member',
                description='The member of whose balance to update.',
                required=False)
            ],
        guild_ids=[153689763780624385, 972473224845729802])
    async def addbal(self, ctx: APPCI, amount: int, member: discord.Member = None):
        if ctx.author.id == 911306468106571816:
            with open("root/Satori/info.json", "r") as f:
                users = json.load(f)
            if not member:
                users[str(ctx.author.id)]['Currency'] += amount
                await ctx.respond(f"added {amount} to @{ctx.author}!")

            else:
                users[str(member.id)]['Currency'] += amount
                await ctx.respond(f"added {amount} to @{member}!")
            with open("root/Satori/info.json", "w") as fp:
                json.dump(users, fp, indent=4)

    

    @commands.is_owner()
    @commands.Cog.slash_command(
        name='setchannel',
        description='Sets channel for RealmBlog cog.',
        options=[
          Option(
            option_type=int,
            name='channel',
            description='Channel ID for RealmBlog to send to.',
            required=True)
            ])
    async def setchannel(self, ctx: APPCI, channel_id: int):
        if ctx.author.id == 911306468106571816:
          with open("root/Satori/latest.json", "r") as f:
            latest = json.load(f)
          latest['channel'] = channel_id 
          await ctx.respond("Channel set. Will run blog updates here.")
          with open("root/Satori/latest.json", "w") as fp:
            json.dump(latest, fp, indent=4)

    @commands.is_owner()
    @commands.Cog.slash_command(
      name='sendtonews',
      description='Sends message to #news-updates channel in Death Poets.',
      options=[
        Option(
          option_type=str,
          name='text',
          description='The text you want to send.')],
      guild_ids=[972473224845729802, 374716378655227914])
    async def send_to_news_channel(self, ctx: APPCI, text: str):
        if ctx.author.id == 911306468106571816:
          with open("root/Satori/latest.json", "r") as f:
            latest = json.load(f)
          channel = latest['channel']
          chan = await self.bot.fetch_channel(channel)
          await chan.send(text)
          await ctx.respond("Message sent.")

    @commands.Cog.slash_command(
      name='roleassign',
      description='Button Roles for Death Poets',
      guild_ids=[374716378655227914, 972473224845729802])
    @commands.is_owner()
    async def roleassign(self, ctx: APPCI):
        if ctx.author.id == 911306468106571816:
            guild = await self.bot.fetch_guild(374716378655227914)    
            embed = discord.Embed(title="<:Deathpoets:956438142230097930> Below you will find buttons that'll assign you a role of your choice. <:Deathpoets:956438142230097930>", 
                                description="", color=0x00ff00)
            embed.add_field(name="🎮Epic Gamer🎮", value="Gives you access to the other games text channels.", inline=True)
            embed.add_field(name="🔞NSFW🔞", value="Gives you access to the NSFW channel. This was made because too much nsfw stuff in general.", inline=True)
            embed.add_field(name="?????", value="???????", inline=True)
            embed.set_author(icon_url=guild.icon_url, name="Welcome to DeathPoets!")
    
            components = [ActionRow(Button(label='🎮Epic Gamer🎮',
                                    custom_id='epic_gamer',
                                    style=ButtonStyle.green
                                    ),
                                Button(label='🔞NSFW🔞',
                                    custom_id='nsfw_button',
                                    style=ButtonStyle.green),
                                Button(label='?????',
                                    custom_id='???????',
                                    style=ButtonStyle.green,
                                    disabled=True))
                    ]
            await self.bot.get_channel(1000742060636246126).send(embed=embed, components=components)
            await ctx.respond("`SUCCESS`")

  
    @commands.Cog.slash_command(
      name="whois",
      description='Get user info.',
      options=[
        Option(
          option_type=discord.Member,
          name='member',
          description='The user whose info  is wanted.')])
    @commands.is_owner()
    async def who_is(self, ctx: APPCI, member: discord.Member):
        try:
            user = await self.bot.fetch_user(int(id))
            member = ctx.message.guild.get_member(id)
        except Exception as e:
            await ctx.respond(f"Error: {e}")
            return
        else:
            embed = discord.Embed(title=f"Showing info for {id}", description="", color =0x00ff00)
            if not member.nick:
              embed.add_field(name="User's Name", value=f"{str(member)}", inline=True)
            else:
              embed.add_field(name="User's Name", value=f"{user.name}#{user.discriminator}({member.nick})", inline=True)
            embed.add_field(name="Created at:", value=user.created_at, inline=True)
            if user in ctx.message.guild.members:
              embed.add_field(name="Joined at", value=member.joined_at, inline=True)
            embed.set_author(icon_url=user.avatar_url, name=f"User request for {str(ctx.message.author)}")
            await ctx.respond(embed=embed)
            #await ctx.send(f"{user.name}#{user.discriminator} ({user.id})\n{user.avatar_url}\n{user.created_at}")


    @commands.Cog.slash_command(
      name="json",
      description='Updates whatever json needs to be updated.')
    async def json_update(self, ctx:APPCI):
        with open("root/Satori/logs.json", "r") as f:
          logs = json.load(f)
        guild = self.bot.get_guild(374716378655227914) 
        staff_role = discord.utils.get(guild.roles, name="Staff")
        leader_role = discord.utils.get(guild.roles, name="Leader")
        founder_role = discord.utils.get(guild.roles, name="Founder")
        roles = [staff_role, leader_role, founder_role]
        guild_users=[]
        for x in guild.members:
          if any(y in x.roles for y in roles):
              guild_users.append(x)
        a=[]
        for user in guild_users:
          if str(user.id) in str(logs):
              await ctx.respond(f'{user.id} found! skipping.')
          else:
              logs[str(guild.id)]['Users'][f'{user.id}'] = {}
              logs[str(guild.id)]['Users'][f'{user.id}']['Name'] = user.name
              logs[str(guild.id)]['Users'][f'{user.id}']['Accepted'] = 0
              logs[str(guild.id)]['Users'][f'{user.id}']['Declined'] = 0  
              a.append(user)
        with open("root/Satori/logs.json", "w") as fp:
          json.dump(logs, fp, indent=4)
        await ctx.respond('Done! :thumbsup:')
  

    @commands.Cog.slash_command(
      name="test",
      description='Test command that changes frequently')
    async def test_com(self, ctx:APPCI):
        # dong = []
        # for a in ctx.guild.members:
        #   dong.append(a)
        await ctx.respond(*ctx.guild.members)



        '''This gets all msgids, searches for them in every channel to find message. Kinda obnsolete.'''
        # messages = []
        # channels_list = []
        # channels = ctx.guild.channels
        # for channel in channels:
        #   channels_list.append(channel)
        # print(channels)
        # for ids in msgids:
        #   for c in channels:
        #     chaan = self.bot.get_channel(c.id)
        #     try:
        #       e = await chaan.fetch_message(ids)
        #     except:
        #       continue
        #     else:
        #       messages.append(e.content)
              
        #   print(messages)
        #   await ctx.respond(messages)
def setup(bot):
    bot.add_cog(OwnerCog(bot))