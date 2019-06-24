from random import choice
import asyncio
import util.image as image
from util.reddit import reddit


def init(bot, data):
    if "wouldyourather" not in data:
        data["wouldyourather"] = {}
    our_data = data["wouldyourather"]
    
    @bot.command()
    async def wouldyourather(ctx):
        async with ctx.typing():
            threads = list(reddit.subreddit('WouldYouRather').new())
            while True:
                title = choice(threads).title
                title = title.lower().replace("would you rather ", "").replace("wyr ", "").replace("?", "")
                if title.endswith("."):
                    title = title[:-1]
                if ", or " in title:
                    title = title.split(", or ")
                elif " or " in title:
                    title = title.split(" or ")
                else:
                    continue
                break
        
        title = "would you rather " + " or ".join(title) + "?"
        if title not in our_data:
            our_data[title] = [0, 0]
        
        await image.send_image(ctx, title, "white.jpg", "wouldyourather.jpg", (0, 0), 40, (0, 0, 0))
        message = await ctx.send(title)
        await message.add_reaction('1⃣')
        await message.add_reaction('2⃣')
        await asyncio.sleep(0.1)

        def check(emote, user):
            return emote.emoji == '1⃣' or emote.emoji == '2⃣'

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=20, check=check)
        except asyncio.TimeoutError:
            await ctx.send('too slow')
        else:
            if reaction.emoji == '1⃣':
                index = 0
            else:
                index = 1
                
            our_data[title][index] += 1
            total = our_data[title][0] + our_data[title][1]
            percentage = round((our_data[title][index] / total) * 100, 2)
            await ctx.send(str(percentage) + "% agreed with you")
