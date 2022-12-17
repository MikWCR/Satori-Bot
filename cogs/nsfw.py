from discord.ext import tasks, commands
import discord
from discord import SlashCommandOption as Option, Localizations, Permissions, ApplicationCommandInteraction as APPCI
from discord import ActionRow, Button, ButtonStyle
from typing import Optional, List

import random
import urllib.request, json
import asyncio
import requests
import random

class nsfw(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        global accessable_guilds
        accessable_guilds = []
        for guild in self.bot.guilds:
            accessable_guilds.append(guild.id)


    def cog_unload(self):
        self.yand_loop.cancel()

    @tasks.loop(seconds=300)
    async def yand_loop(self):
        r = random.randint(1, 100)
        r2 = random.randint(1, 24)
        channel = await self.bot.fetch_channel(271148913744936970)
        with urllib.request.urlopen(f"https://yande.re/post.json?limit=25&page={r}&tags=rating:e") as url:
            data = json.loads(url.read().decode())
            url = data[r2]['file_url']
            await channel.send(url)

    @commands.Cog.listener()
    async def on_ready(self):
        self.yand_loop.start()


    @commands.Cog.slash_command(
        name='yandere',
        description='Grabs images from yande.re with given tags, page, and index or random safe image.',
        options = [
        Option(
            option_type = str,
            name = 'tags',
            description = 'The tags you want for the image(s). Ex: rating:safe, animal_ears',
            required=False),
        Option(
            option_type=int,
            name='page',
            description='The desired page of images.',
            required=False,
            min_value=1,
            max_value=100),
        Option(
            option_type=int,
            name='index',
            description='Image index from certain page. (1 = first image on page, etc)',
            required=False,
            min_value=1,
            max_value=24)
        ])
    async def yand(self,
                    ctx: APPCI,
                    index: int = None,
                    page: int = None,
                    tags: str = "rating:safe"):
        if not index:
            index = random.randint(1, 24)
        if not page:
            page = random.randint(1, 100)
        tags = tags.split()
        direct_url = "https://yande.re/post/show/"
        args = '+'.join(tags)
        r = random.randint(0, 0xffffff)
        try:
          url, post_id, preview_url, total_tags_first = await grabpic(self, ctx, args, value=index, r=page)
        except Exception as e:
          print(f"Error raised: {e}")
          return
        embed = discord.Embed(title=f"With tags: {', '.join(tags)}", color=r)
        embed.set_author(name=f"Click to go to page.", url=f"{direct_url}{post_id}", icon_url=preview_url)
        embed.set_image(url=url)
        embed.set_footer(text=f"{total_tags_first}")
        components=[ActionRow(
            Button(
                #label="",
                emoji="◀️",
                style=discord.ButtonColor.green,
                custom_id="Left"
                ),
            Button(
                #label="",
                emoji="▶️",
                style=discord.ButtonColor.red,
                custom_id="Right"
                ))
                ]
        msg = await ctx.respond(embed=embed, components=components)
        sec_msg = await ctx.respond(f"searching {args}, on page {page}, index: {index}")
        while True:
            try:
                def _check(i: discord.ComponentInteraction, b):
                    return i.message == msg and i.author == ctx.author
                interaction, button = await self.bot.wait_for('button_click', check=_check, timeout=20.0)
                await interaction.defer()
                if button.custom_id == 'Right':
                    #Right Button Clicked
                    if index >= 24:
                        await interaction.channel.send("You have reached the end of this list, please run the command again.")
                        return
                    new_embed = discord.Embed(title=f"With tags: {', '.join(tags)}", color=r)
                    index += 1
                    newurl, id, preview, total_tags = await grabpic(self, ctx, args=args, value=index, r=page)
                    new_embed.set_author(name=f"Click to go to page.", url=f"{direct_url}{id}", icon_url=preview)
                    new_embed.set_image(url=newurl)
                    new_embed.set_footer(text=f"{total_tags}")
                    await interaction.edit(embed=new_embed, components = components)
                    await sec_msg.edit(content=f"searching {', '.join(tags)}, on page {page}, index: {index}")
                else:
                    #Left Button Clicked
                    index -= 1
                    oldurl, oldid, oldpreview, old_total_tags  = await grabpic(self, ctx, args=args, value=index, r=page)
                    back_emb = discord.Embed(title=f"With tags: {', '.join(tags)}", color=r)
                    back_emb.set_author(name=f"Click to go to page.", url=f"{direct_url}{oldid}", icon_url=oldpreview)
                    back_emb.set_image(url=oldurl)
                    back_emb.set_footer(text=f"{old_total_tags}")
                    await sec_msg.edit(content=f"searching {', '.join(tags)}, on page {page}, index: {index}")
                    await interaction.edit(embed=back_emb, components=components)
            except asyncio.TimeoutError:
                return
async def grabpic(self, ctx, args, value, r):
   #print(f" tags = {args} value= {value} page = {r}")
    with urllib.request.urlopen(f"https://yande.re/post.json?limit=25&page={r}&tags={args}") as url:
        data = json.loads(url.read().decode())
        if not data:
            with urllib.request.urlopen("https://yande.re/tag.json?limit=100&order=count") as tag_url:
                tag_data = json.loads(tag_url.read().decode())
            tags = []
            
            for i in range(len(tag_data)):
              tags.append(tag_data[i]['name'])
                
            await ctx.channel.send(f"Invalid tags: `{args}.`\nExample tags: ```{random.sample(tags, 25)}```")
            return False
        try:
            url = data[value]['sample_url']
        except:
            value = 1
            await ctx.channel.send("Invalid Index found on page. Setting index to 1.")
            url = data[value]['sample_url']

        id = data[value]['id']
        preview_url = data[value]['preview_url']
        try:
          total_tags = data[value]['tags']
        except:
          total_tags= 'none'
    #print(f"{url} {id} {preview_url} {total_tags}")
    return url, id, preview_url, total_tags

def setup(bot):
    bot.add_cog(nsfw(bot))