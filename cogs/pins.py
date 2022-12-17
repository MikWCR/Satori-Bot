import discord

import json
from discord.ext import commands
from discord import SlashCommandOption as Option, Localizations, Permissions, ApplicationCommandInteraction as APPCI, ActionRow, Button, ButtonStyle
from api.rotmgblog import BlogApi
import random
import re
from datetime import datetime
from pytz import timezone
import asyncio

'''Module for pinning messages with Pushpin emoji.'''
class PinCog(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
      if reaction.emoji == "📌":
        guildid = str(reaction.message.guild.id)
        with open("root/Satori/pins.json", "r") as f:
            pins = json.load(f)      
        if reaction.count > 1:
            return
        else:
            msgid = reaction.message.id
            dte = reaction.message.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))
            dt = reaction.message.created_at.now()
            if not guildid in pins:
                pins[guildid] = {}
            if str(msgid) in str(pins[guildid]):
                await reaction.message.channel.send("stupid bitch it already pinned nigga LMAAO u fuckin dum")
                return
            obj = len(pins[guildid])
            if len(pins[guildid]) < 1:
                obj = obj+1
            obj = len(pins[guildid])+1
            pins[guildid][obj] = {}
            pins[guildid][obj]['author'] = reaction.message.author.name
            pins[guildid][obj]['authorid'] = reaction.message.author.id
            pins[guildid][obj]['content'] = reaction.message.content
            pins[guildid][obj]["url"] = reaction.message.jump_url
            pins[guildid][obj]['date'] = dte.strftime("%m/%d/%Y, %H:%M:%S")
            pins[guildid][obj]['pinner'] = user.name
            pins[guildid][obj]['pinnerid'] = user.id
            pins[guildid][obj]['pindate'] = dt.strftime("%m/%d/%Y, %H:%M:%S")
            pins[guildid][obj]['msgid'] = str(reaction.message.id)
            pins[guildid][obj]['channel'] = reaction.message.channel.name
            pins[guildid][obj]['embed'] = False
            if reaction.message.embeds:
                pins[guildid][obj]['embed'] = True
                embe = reaction.message.embeds
                for embed in embe:
                    e = embed.to_dict()
                    try:
                        try:
                            pins[guildid][obj]['content'] = e['url']
                        except:
                            pins[guildid][obj]['content'] = e['image']['url']
                    except:
                        pins[guildid][obj]['content'] = e['description']
            if len(reaction.message.attachments) > 0:
                attachment = reaction.message.attachments[0]
                pins[guildid][obj]['content'] = attachment.url
            with open("root/Satori/pins.json", "w+") as fp:
                json.dump(pins, fp, indent=4)
            await reaction.message.reply(f"Message pinned. Use /pins. Total pins {len(pins[guildid])}")
            return
    @commands.Cog.slash_command(
        base_name='pins',
        base_desc='Shows most recent pins, or a given pin. Pin a message with 📌.',
        name='show',
        description = 'Shows most recent pins, or a given pin. Pin a message with 📌.',
        options=[
          Option(
            option_type=int,
            name='pin_number',
            description='The pin number you want to view. (1 for the first pin)',
            required=False)])
    async def pins_show(self, ctx: APPCI, pin_number: int = None):
      with open("root/Satori/pins.json", "r+") as f:
        p = json.load(f)
        guild_id = str(ctx.guild.id)
      if not guild_id in str(p):
        await ctx.respond("Server not found. Please pin a message first.")
        return
      if not pin_number:
        embed = discord.Embed(title=f"Most recent pins:", description=f'Use "/pins show (pin_number)" |{discord.utils.styled_timestamp(datetime.now(), "R")}', color=random.randint(0, 0xffffff))
        authors, content, dates, urls = [], [], [], []
        for a in p[guild_id]:
            authors.append(p[guild_id][a]['author'])
            content.append(p[guild_id][a]['content'])
            dates.append(p[guild_id][a]['date'])
            urls.append(p[guild_id][a]['url'])
            #print(msgids)
            continue
        try:
            nc = content[-6:]
            na = authors[-6:]
            nd = dates[-6:]
            nu = urls[-6:]
        except:
            nc = content[-len(content):]
            na = authors [-len(authors):]
            nd = dates[-len(dates):]
            nu = dates[-len(urls):]
        await ctx.respond(f"No parameter, showing {len(nc)} latest pins.")
        for i in range(len(nc)):
            embed.add_field(name=f"{na[i]} on {nd[i]}", value=f'"[{nc[i]}]({nu[i]})"', inline= True)
            embed.set_footer(text=f"Total pins: {str(len(p[guild_id]))}", icon_url="")
        await ctx.respond(embed=embed)
        return
       # await ctx.respond(discord.utils.styled_timestamp(datetime.now(), discord.TimestampStyle.long))
      elif int(pin_number) > 0:
          embed = await get_pin(self, p, guild_id, pin_number)
          await ctx.respond(embed=embed, components= [])
    @commands.Cog.slash_command(
        base_name='pins',
        base_desc='Searches for a pin.',
        name = 'search',
        description = 'Searches for a pin.',
        options=[
          Option(
            option_type=str,
            name='phrase',
            description='What you want to search for.',
            required=True)])
    async def pins_search(self, ctx: APPCI, phrase: str = None):
      with open("root/Satori/pins.json", "r+") as f:
        p = json.load(f)
      msg = await ctx.respond(f'Searching for `{phrase}`')
      guild_id = str(ctx.guild.id)
      embed = discord.Embed(title=f"Search results for {phrase}:", description=f'{discord.utils.styled_timestamp(datetime.now(), "R")}', color=random.randint(0, 0xffffff))
      key, authors, contents, dates, urls = [], [], [], [], []
      if not guild_id in str(p):
          await ctx.respond("Server not found. Please pin a message first.")
          await msg.delete()
          return
      for a in p[guild_id]:
        if phrase in p[guild_id][a]['content']:
            authors.append(p[guild_id][a]['author'])
            contents.append(p[guild_id][a]['content'])
            dates.append(p[guild_id][a]['date'])
            urls.append(p[guild_id][a]['url'])
            key.append(a)
            continue
        continue
      if phrase in str(contents):
        async with ctx.channel.typing():
          await asyncio.sleep(1.7)
        await ctx.respond(f"Found {len(contents)} results.")
        if len(contents) >= 20:
          contents = contents[-20:]
          authors = authors[-20:]
          dates = dates[-20:]
          urls = urls[-20:]
          await ctx.respond("Too many results, showing the latest 20 pins.")
        for i in range(len(contents)):
            embed.add_field(name=f"{authors[i]} on {dates[i]} (Pin #{key[i]})", value=f'"[{contents[i]}]({urls[i]})"', inline= True)
        embed.set_footer(text=f"Total pins: {str(len(p[guild_id]))}. Use /pins show (pin number) to view full information.", icon_url="")
        await msg.edit(embed=embed)
        return
      else:
        await msg.edit(content=f"No results found for `{phrase}`.")
        await asyncio.sleep(10)
        await msg.delete()

    @commands.Cog.slash_command(
        base_name='pins',
        base_desc='Removes a pin.',
        name = 'remove',
        description = 'Removes pin given. Only works if you\'re the pinner or author of the pin.',
        options=[
          Option(
            option_type=int,
            name='pin_number',
            description='The pin number you\'d like to remove.',
            min_value='1',
            required=True)])
    async def pins_remove(self, ctx: APPCI, pin_number: int = None):
      with open("root/Satori/pins.json", "r+") as f:
        p = json.load(f)
      guild_id = str(ctx.guild.id)
      if pin_number > len(p[guild_id]):
        await ctx.respond(f'There are only {len(p[guild_id])} pins. Try again.', hidden=True, delete_after=5)
        return
      pinnerid = p[guild_id][str(pin_number)]['pinnerid']
      authorid = p[guild_id][str(pin_number)]['authorid']
      if ctx.author.id == pinnerid or ctx.author.id == authorid or ctx.author.guild_permissions.manage_messages:
        embed = await get_pin(self, p=p, guild_id=guild_id, pin_number=pin_number)
        emb_msg = await ctx.respond(embed=embed)
        components = [
          ActionRow(
            Button(label='Yes',
              custom_id='yes_button',
              style=ButtonStyle.green),
            Button(label='No',
              custom_id='no_button',
              style=ButtonStyle.red))
              ]
        component_msg = await ctx.channel.send(f'Are you sure you want to delete this pin?', components=components)
        def _check(i: discord.ComponentInteraction, b):
            return i.message == component_msg and i.member == ctx.author and i.channel == ctx.channel
        while True:
          try:
              interaction, button = await self.bot.wait_for('button_click', check=_check, timeout=10)
              button_id = button.custom_id
              if button_id == "yes_button":
                await component_msg.edit(content=f'Attempting to remove Pin #`{pin_number}`...', components=[])
                async with ctx.channel.typing():
                  await asyncio.sleep(2)
                  del p[guild_id][str(pin_number)]
                  for key, values in list(p[guild_id].items()):
                      if int(key) > int(pin_number):
                          p[guild_id][str(int(key)-1)] = p[guild_id].pop(str(key))
                  with open("root/Satori/pins.json", "w+") as fp:
                      json.dump(p, fp, indent=4)
                  await ctx.respond(f'Pin {pin_number} has been removed!', delete_after=5)
                  await component_msg.delete()
                  await emb_msg.delete()
                  return
              else:
                  await ctx.respond("Pin not deleted.", hidden=True, delete_after=5)
                  return
          except asyncio.TimeoutError:
              await ctx.respond("Timed out waiting for response. Remove request cancelled.", hidden=True, delete_after=5)
              await component_msg.delete()
              await emb_msg.delete()
              return
        return
      else:
        await ctx.respond('You do not have permission to remove this pin. Only the pinner or the pin author can remove. Or have manage_messages permission.', hidden=True, delete_after=5)


async def get_pin(self, p, guild_id, pin_number):
  author = p[guild_id][str(pin_number)]['author']
  content = p[guild_id][str(pin_number)]['content']
  url = p[guild_id][str(pin_number)]['url']
  date = p[guild_id][str(pin_number)]['date']
  pindate = p[guild_id][str(pin_number)]['pindate']
  pinner = p[guild_id][str(pin_number)]['pinner']
  channel = p[guild_id][str(pin_number)]['channel']
  emb = p[guild_id][str(pin_number)]['embed']
  embed = discord.Embed(title=f"Message from {author} in {channel}", description=f'"{content}"', color=random.randint(0, 0xffffff))
  embed.add_field(name=f"Pinned by {pinner} on ", value=f"{pindate}", inline=False)
  embed.set_footer(text=f"Message date: {date}", icon_url="")
  embed.set_author(name=f"Pinned message #{pin_number}. Click to go to original", url=url,
  icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/mozilla/36/pushpin_1f4cc.png")
  matches = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
  if any(x in str(content) for x in matches):
    print("Image!!!")
    embed.set_image(url=content)
  return embed
def setup(bot):
  bot.add_cog(PinCog(bot))