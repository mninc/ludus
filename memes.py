from random import choice
from util.reddit import reddit
from util.image import download_image


async def get_meme(ctx, subreddit):
    async with ctx.typing():
        threads = list(reddit.subreddit(subreddit).new())
        while True:
            thread = choice(threads)
            if not thread.url or thread.over_18:
                continue
            if not await download_image(ctx, thread.url):
                continue
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
    async def me_irl(ctx):
        await get_meme(ctx, 'me_irl')

    @bot.command()
    async def historymeme(ctx):
        await get_meme(ctx, 'historymemes')
    
    @bot.command()
    async def comedyheaven(ctx):
        await get_meme(ctx, 'comedyheaven')
    
    # can add many more
