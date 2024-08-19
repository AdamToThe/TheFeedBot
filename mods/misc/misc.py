from discord.ext import commands
#import quantumrandom as rand
import secrets as rand 
from roblox import Client

client = Client()

accounts_2017 = ()
with open('mods/misc/data/roblox.txt') as fp:
    accounts_2017 = fp.read().splitlines()


class MiscCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='2017')
    @commands.is_owner()
    async def _(self, ctx):
        a = rand.choice(accounts_2017).split(':')
        usr, pss = tuple(a)

        user = await client.get_user_by_username(usr, expand=True)

        return await ctx.message.reply(
            '\n'.join(
                [f'**__Username__**:  {usr}', f'**__Password__ **:  {pss}',
                f'**__PROFILE__**: https://roblox.com/users/{user.id}/profile', '```',
                f'ID: {user.id}', f'Display Name: {user.display_name}', '```']
            ),
            mention_author=False)
      
