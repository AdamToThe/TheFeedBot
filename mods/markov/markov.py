from discord.ext import commands
from .markov_chain import Markov
from markovchain.text import ReplyMode

from typing import Union
import discord as cord
import random
import funcs
import re
import colorama

class MarkovCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.b = Markov()
        self.ats = open('mods/markov/data/attachs.txt').read().splitlines()
        

    @commands.Cog.listener()
    async def on_message(self, msg):
        content = msg.content
        mention = self.bot.user.mention
        after_mention = content[len(mention):]

        chnce = random.random()
        print(f'{msg.author} chance: {chnce*100}/100')
        
        ctx = await self.bot.get_context(msg)

        if ctx.valid or msg.author == self.bot.user:
            return

        if msg.channel.id in self.bot.gcs and (content.startswith(mention) or chnce > 0.979):
            t = self.speak()#b.other(reply_mode=ReplyMode.END,
            #reply_to=(after_mention or None))
            print(colorama.Fore.RED, 'SAYING: ', colorama.Fore.GREEN, t, colorama.Fore.RESET)
            clean = re.sub(r'<@.*>', '', t)
            
            return await msg.channel.send(clean)

        self.learn(msg)
        self.save_msg(msg)
        

    @commands.command(aliases=['random'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def rand(self, ctx):
        w = random.choice(self.ats)
        b = funcs.download_bytes(w)
        mime, ext = funcs.get_mime(w)
        try:
            await ctx.message.reply(file=cord.File(b, f'WeskerAutism{ext}'),
                                mention_author=False)
        except:
            await ctx.message.reply(f'> I COULDN\'T SEND ATTACH-EXPLICIT\n{w}',
                                mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def corpus(self,
                    ctx,
                    channel: Union[cord.TextChannel,
                                   cord.GroupChannel] = None):
        channel = ctx.channel if channel is None else channel
        async for msg in channel.history(limit=70000, before=ctx.message):
            self.learn(msg)
            self.save_msg(msg)
            del msg

        await ctx.message.add_reaction('👾')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, channel: Union[cord.TextChannel,
                                   cord.GroupChannel] = None):
        channel = ctx.channel if channel is None else channel
        async for msg in channel.history(limit=70000):
            self.save_msg(msg)
            del msg
        await ctx.message.add_reaction('⬇️')    

    def speak(self, *a, **kw):
        v = self.b(max_words=16, *a, **kw)
        if not v:
            return self.speak(*a, **kw)
        return v
    
    def learn(self, msg):
        if msg.author.id == 1081004946872352958 or msg.author.bot:  #CLYDE BITCH
            return
        self.b.learn(msg.content)

    def save_msg(self, msg):
        fp = funcs.get_files_from(msg,
                                 image=True,
                                 video=True,
                                 no_tenor=True)
        for url in fp:
            self.b.write_to('attachs.txt', url)
        del msg