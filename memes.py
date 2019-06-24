from random import choice
from util.reddit import reddit
from util.image import random_name
import requests
import discord
import shutil


async def get_meme(ctx, subreddit):
    async with ctx.typing():
        threads = list(reddit.subreddit(subreddit).new())
        while True:
            thread = choice(threads)
            if not thread.url or thread.over_18:
                continue
            file_type = thread.url.split(".")
            file_type = file_type[len(file_type) - 1]
            r = requests.get(thread.url, stream=True)
            path = "./images/" + await random_name() + "." + file_type
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            with open(path, "rb") as picture:
                await ctx.send(file=discord.File(picture, 'meme.' + file_type))
            break


def init(bot, data):
    @bot.command()
    async def meme(ctx):
        await get_meme(ctx, 'memes')
    
    @bot.command()
    async def dankmeme(ctx):
        await get_meme(ctx, 'dankmemes')

    @bot.command()
    async def prequelmeme(ctx):
        await get_meme(ctx, 'prequelmemes')

    @bot.command()
    async def i_irl(ctx):
        await get_meme(ctx, 'i_irl')

    @bot.command()
    async def me_irl(ctx):
        await get_meme(ctx, 'me_irl')

    @bot.command()
    async def historymeme(ctx):
        await get_meme(ctx, 'historymemes')
    
    # can add many more
