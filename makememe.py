from util.image import download_image, centre_image
import aiohttp
import json

with open("config.json") as f:
    config = json.load(f)


formats = {
    "drake": 181913649,
    "twobuttons": 87743020,
    "simply": 61579,
    "spongebob": 102156234,
    "button": 119139145,
    "everywhere": 91538330,
    "pooh": 178591752,
    "wesmart": 89370399,
    "harold": 27813981,
    "fry": 61520,
    "trump": 91545132,
    "kermit": 84341851
}


def init(bot, data):
    @bot.command(aliases=["make_meme"])
    async def makememe(ctx, *args):
        if len(args) == 1 and args[0] == "formats":
            text = ["Formats:"]
            text += formats.keys()
            await centre_image(ctx, text, 'scroll_large.png', 30, (0, 0, 0))
            return
        
        if len(args) != 3:
            await ctx.send(ctx.author.mention + ": incorrect number of arguments! Check >help for info.")
            return
        if args[0].lower() not in formats:
            await ctx.send(ctx.author.mention + ": invalid format! Do >makememe formats")
            return
        
        async with ctx.typing():
            url = "https://api.imgflip.com/caption_image"
            template_id = formats[args[0].lower()]
            line1 = args[1]
            line2 = args[2]
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, params={
                    "username": config["imgflip_username"],
                    "password": config["imgflip_password"],
                    "template_id": template_id,
                    "text0": line1,
                    "text1": line2
                }) as response:
                    r = await response.json()
                    image_url = r["data"]["url"]
                    await download_image(ctx, image_url)
