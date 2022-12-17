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
import re

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.slash_command(
        name='balance',
        description="The amount of munnies you have or a given users.",
        options = [
            Option(
                option_type=discord.Member,
                name='member',
                description='The user of whose balance to show.',
                required=False)
        ],
        guild_ids=[153689763780624385, 972473224845729802]
        )
    async def balance(self, ctx: APPCI, member: discord.Member=None):
        with open("root/Satori/info.json", "r") as f:
            users = json.load(f)
        if not member:
          currency = users[str(ctx.author.id)]['Currency']
          await ctx.respond(f"Balance: {currency} ₘᵤₙₙᵢₑₛ")
        else:
            try:
              member_currency = users[str(member.id)]['Currency']
                #mentionid = re.findall(r'\b\d+\b', member)
                #userbal = users[str(mentionid[0])]['Currency']
            except:
                await ctx.respond("User not found in database. Most likely never spoke or a mf robot.")
                return
            else:
              await ctx.respond(f"{member}'s balance: {member_currency}")

def setup(bot):
    bot.add_cog(EconomyCog(bot))