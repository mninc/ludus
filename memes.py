from random import choice
from util.reddit import reddit
import discord


async def get_meme(ctx, subreddit):
    # get random thread in the newest posts in the subreddit and if it has an image, post it in an embed
    await ctx.trigger_typing()
    threads = list(reddit.subreddit(subreddit).new())
    while True:
        thread = choice(threads)
        if not thread.url or thread.over_18:
            continue
        if "imgur.com" in thread.url and "i.imgur.com" not in thread.url:  # deal with non-image imgur links
            thread.url += ".png"
        embed = discord.Embed(title=thread.title,
                              url="https://www.reddit.com" + thread.permalink,
                              colour=0xffffff)
        embed.set_image(url=thread.url)
        await ctx.send(embed=embed)
        return


async def get_joke(ctx, subreddit):
    # get random thread in the newest posts in the subreddit and if it has a body, post it in an embed
    await ctx.trigger_typing()
    threads = list(reddit.subreddit(subreddit).new())
    while True:
        thread = choice(threads)
        if not thread.selftext or thread.over_18:
            continue
        embed = discord.Embed(title=thread.title,
                              url="https://www.reddit.com" + thread.permalink,
                              description=thread.selftext,
                              colour=0xffffff)
        await ctx.send(embed=embed)
        return


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
    
    @bot.command()
    async def joke(ctx):
        await get_joke(ctx, 'jokes')
    
    @bot.command()
    async def dirtyjoke(ctx):
        await get_joke(ctx, 'dirtyjokes')
    
    @bot.command()
    async def cleanjoke(ctx):
        await get_joke(ctx, 'cleanjokes')
    
    @bot.command()
    async def antijoke(ctx):
        await get_joke(ctx, 'antijokes')
    
    @bot.command()
    async def webcomic(ctx):
        await get_meme(ctx, 'webcomics')
    
    @bot.command()
    async def comic(ctx):
        await get_meme(ctx, 'comics')
    
    # could add many more
