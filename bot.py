from discord.ext import commands
from dhooks import Webhook, File as WFile

import discord as cord
import os
import io
#import keep_alive
import asyncio
import funcs

users_blacklist = [
    1045969096396771328  # OTIOPO
]

weskerns_o = [
    802939790789705739,  # WESKER
    1008761926513348608  # S_O
]

gc_whitelist = [
    1129435767073144932,  # MAIN
    1130150267724251197,  # TEST G
    #1102165908492927039   # some server
]

bot = commands.Bot(command_prefix=commands.when_mentioned_or('~'),
                   owner_ids=weskerns_o)

snipes = {}
mimics = {}
mimic_targets = []

dump_hooks = {
    '🌟': os.environ.get('hook-main'),
    '🍆': os.environ.get('hook-thug'),
    '👤': os.environ.get('hook-personal')
}

bot.remove_command('help')
bot.gcs = gc_whitelist


@bot.event
async def on_ready():
    bot.main_gc = await bot.fetch_channel(gc_whitelist[0])
    for instance in os.listdir('mods'):
        if not instance.startswith('__'):
            await bot.load_extension(f'mods.{instance}')


@bot.check
def check(ctx):
    return ctx.author.id in weskerns_o or ctx.channel.id in gc_whitelist and ctx.author.id not in users_blacklist


@bot.listen()
async def on_raw_reaction_add(raw):
    e = raw.emoji
    es = str(e)

    if raw.user_id in weskerns_o:
        hook = dump_hooks.get(es)

        if es == '⏫':
            user = await bot.fetch_user(raw.user_id)
            channel = await bot.fetch_channel(raw.channel_id)
            msg = await channel.fetch_message(raw.message_id)
            fs = funcs.get_files_from(msg,
                                      image=True,
                                      video=True,
                                      no_tenor=True)
            files = []
            for url in fs:
                b = funcs.download_bytes(url)
                mime, ext = funcs.get_mime(url)
                f = cord.File(b, filename=f'WeskerAutism{ext}')
                files.append(f)
            try:
                q = await bot.main_gc.send(f'SENT BY: @**{user}**',
                                           files=files)
            except Exception as ex:
                if 'explicit' in str(ex).lower():
                    q = await bot.main_gc.send(
                        'SENT BY: @**{0}**\n{1}'.format(user, '\n'.join(fs)))
                else:
                    raise ex

            await q.add_reaction('⭐')
            return

        if hook is None:
            return

        hook = Webhook.Async(hook)

        user = await bot.fetch_user(raw.user_id)
        channel = await bot.fetch_channel(raw.channel_id)
        msg = await channel.fetch_message(raw.message_id)

        fs = funcs.get_files_from(msg, image=True, video=True, no_tenor=True)
        for url in fs:
            b = funcs.download_bytes(url)
            mime, ext = funcs.get_mime(url)
            f = WFile(b, name=f'WeskerAutism{ext}')

            await hook.send(file=f,
                            avatar_url=user.display_avatar.url,
                            username='@{0}{1}'.format(
                                user.name, f'#{user.discriminator}'
                                if user.discriminator != 0 else ''))
            hook.close()


@bot.event
async def on_command_error(ctx, err):
    ignore = ()  #commands.CommandNotFound, )
    if isinstance(err, ignore):
        return

    if isinstance(err, commands.CommandOnCooldown):
        await ctx.message.reply('shh lil nigga',
                                mention_author=False,
                                delete_after=err.retry_after)
        return

    raise err


@bot.listen()
async def on_message(msg):
    cont = msg.content.lower()

    if msg.author.id == bot.user.id:
        return

    if msg.author.id in mimic_targets:
        files = [await x.to_file() for x in msg.attachments]

        mimic = await msg.reply(content=msg.content,
                                files=files,
                                mention_author=False)
        mimics[msg.id] = mimic


#@bot.command()
#@commands.is_owner()
#async def j(ctx, url: str):
#   await bot.accept_invite(url)
#   await ctx.reply(f'*Joined* ✅:\n{url}')


@bot.listen()
async def on_message_delete(msg):
    files = []
    content = str(msg.content).replace('`', '\\`')
    for at in msg.attachments:
        buffer = io.BytesIO(await at.read())
        files.append(cord.File(buffer, filename=at.filename))

    #snipes[msg.channel.id] = {
    #    'content':
    #    bot.cnv_dict(author=f'{msg.author.name}#{msg.author.discriminator}',
    #                   content=content),
    #    'files':
    #    files
    #}

    if msg.id in mimics:
        await mimics.get(msg.id).delete()
        del mimics[msg.id]


@bot.listen()
async def on_message_edit(bef, msg):
    if msg.id in mimics:
        message = mimics.get(msg.id)
        files = [await x.to_file() for x in msg.attachments]

        await message.edit(content=msg.content, attachments=files)


@bot.command()
@commands.is_owner()
async def mimic(ctx, target: cord.User):
    if target.id == bot.user.id:
        return await ctx.reply(
            'i don\'t support self-hate/haram unless you\'re otiopo')
    if target.id in mimic_targets:
        mimic_targets.remove(target.id)
        return
    mimic_targets.append(target.id)


@bot.command(aliases=['ss', 'sc'])
@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
async def screenshot(ctx, url: str):
    if not url.startswith('http') or not url.startswith('https'):
        url = f'https://{url}'
    requrl = f'https://image.thum.io/get/width/1020/crop/768/maxAge/12/noanimate/{url}'
    r = await bot.get_content(requrl)
    buffer = io.BytesIO(r)
    await ctx.reply(file=cord.File(buffer, filename='screenshot.png'),
                    mention_author=False)


@bot.command()
async def snipe(ctx):
    snipe = snipes.get(ctx.channel.id)
    if not snipe:
        return await ctx.message.add_reaction('❌')

    await ctx.reply(mention_author=False, **snipe)


if __name__ == '__main__':
    keep_alive.keep_alive()
    #   os.system('rm tmp/*/* & rm tmp/*.*')
    bot.run(os.environ.get('T'))
                                             
