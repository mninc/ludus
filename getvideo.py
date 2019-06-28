import aiohttp
import json
from random import choice


with open("config.json") as f:
    config = json.load(f)


def init(bot, data):
    @bot.command()
    async def trending(ctx, country_code="US"):
        # check country code
        if len(country_code) != 2:
            await ctx.send(ctx.author.mention + ": Country code must be two characters long!")
            return
        
        # get result from api
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/youtube/v3/videos", params={
                "part": "id",
                "chart": "mostPopular",
                "regionCode": country_code.upper(),
                "maxResults": 25,
                "key": config["youtube_api_key"]
            }) as response:
                r = await response.json()
                video = choice(r["items"])
                await ctx.send("https://youtube.com/watch?v=" + video["id"])
    
    @bot.command(aliases=["yt"])
    async def youtube(ctx, query):
        # get result from api
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/youtube/v3/search", params={
                "part": "id",
                "maxResults": 1,
                "order": "relevance",
                "q": query,
                "type": "video",
                "key": config["youtube_api_key"]
            }) as response:
                r = await response.json()
                video = r["items"][0]["id"]["videoId"]
                await ctx.send("https://youtube.com/watch?v=" + video)
