import discord, json
from discord import (
    SlashCommandOption as Option,
    ApplicationCommandInteraction as APPCI
)
from discord.ext import commands
import random




class LogKeyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.slash_command(
        description='Log a key popped for the guild.',
        options=[
            Option(
                name='user',
                description='The user which popped like a chad',
                option_type=discord.Member,
                required=True
            ),
            Option(
                name='keys',
                description='Amount of keys popped',
                option_type=int,
                required=True
            )
        ],
        guild_ids=[374716378655227914, 972473224845729802],
        default_required_permissions=discord.Permissions(use_application_commands=True)
    )

    #rl and staff roles required
    @commands.has_any_role(1140088001242861719, 1035031466809233418, 1000872240763646012)
    async def logkey(self, ctx: APPCI, user: discord.Member, keys: int):
        guild_ID = str(ctx.guild_id)
        with open("root/Satori/keys.json", "r") as f:
            key_data = json.load(f)

        if not str(ctx.guild.id) in str(key_data):
                
                key_data[guild_ID] = {}

        
        keypopper = user.id

        if str(keypopper) in str(key_data[guild_ID]):
            key_data[guild_ID][str(keypopper)]["Keys"] = int(key_data[guild_ID][str(keypopper)]["Keys"])+keys
        
        else:
            key_data[guild_ID][str(keypopper)] = {}
            if user.nick:
                key_data[guild_ID][str(keypopper)]['Nick'] = user.nick
            key_data[guild_ID][str(keypopper)]['Name'] = user.name
            key_data[guild_ID][str(keypopper)]['Keys'] = keys


    
        with open('root/Satori/keys.json', 'w+') as file:
            json.dump(key_data, file, indent=4)

        keys_popped =  key_data[guild_ID][str(keypopper)]["Keys"]

        #rich embed
        if keys > 1:
            title = 'Keys'
        else:
            title = 'Key'
        embed = discord.Embed(title=f"{title} logged!", description=f"{user.mention} popped {keys} {title.lower()}. Total: {keys_popped}", color=random.randint(0, 0xffffff))


        await ctx.respond(embed=embed)
        
        
        
        try:
            role_poet = ctx.guild.get_role(1160934593331986552)
            role_veteran = ctx.guild.get_role(1160934911738396772)
            role_master = ctx.guild.get_role(1161153008474792076)
            role_king = ctx.guild.get_role(1161153063030116362) #
            role_divine = ctx.guild.get_role(1161153110677401600)
        except Exception as e:
            await ctx.respond(f'Roles are not found in this server. \n `{e}`', hidden=True)
            return
    

        rolee=ctx.guild.get_member(keypopper)
    


        if keys_popped >= 500:
            if role_divine not in rolee.role_ids:
                await rolee.add_roles(role_divine)
            

        if keys_popped >= 250:
            if role_king not in rolee.role_ids:
                await rolee.add_roles(role_king)
            

        if keys_popped >= 100:
            if role_master not in rolee.role_ids:
                await rolee.add_roles(role_master)
            

        if keys_popped >= 50:
            if role_veteran not in rolee.role_ids:
                await rolee.add_roles(role_veteran)
            

        if keys_popped >= 25:
            if role_poet not in rolee.role_ids:
                await rolee.add_roles(role_poet)


        #await ctx.respond(f"{user.mention} popped {keys} keys.")



    @logkey.error
    async def logkey_error(cog, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingAnyRole):
            await ctx.respond("You are not allowed to do that.", hidden = True)
        # else:
        #     print(f"!{cog}! #{ctx}# ${error}$")





def setup(bot):
    bot.add_cog(LogKeyCommand(bot))
