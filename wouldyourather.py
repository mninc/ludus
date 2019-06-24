from random import choice
import asyncio
import util.image as image
from util.reddit import reddit
from textwrap import wrap
from time import time


def init(bot, data):
    if "wouldyourather" not in data:
        data["wouldyourather"] = {}
    our_data = data["wouldyourather"]
    
    @bot.command()
    async def wouldyourather(ctx):
        async with ctx.typing():
            threads = list(reddit.subreddit('WouldYouRather').new())
            while True:
                thread = choice(threads)
                if thread.over_18:
                    continue
                title = thread.title
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
        
        single_title = " or ".join(title) + "?"
        if single_title not in our_data:
            our_data[single_title] = [0, 0]
        
        first = title[0]
        second = title[1]
        text = wrap(first, 40) + ["or"] + wrap(second, 40)
        
        message = await image.centre_image(ctx, text, "white.jpg", 40, (0, 0, 0), 0)
        await message.add_reaction('1⃣')
        await message.add_reaction('2⃣')
        await asyncio.sleep(0.1)
        
        def check(emote, user):
            return emote.emoji == '1⃣' or emote.emoji == '2⃣'
        
        start_time = time()
        while time() - start_time < 60:
            try:
                reaction, _ = await bot.wait_for('reaction_add', timeout=5, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                async with ctx.typing():
                    if reaction.emoji == '1⃣':
                        index = 0
                    else:
                        index = 1
                    
                    our_data[single_title][index] += 1
                    total = our_data[single_title][0] + our_data[single_title][1]
                    percentage = round((our_data[single_title][index] / total) * 100, 2)
                    await image.centre_image(ctx, [str(percentage) + "% agreed with you"], "white.jpg", 40, (0, 0, 0), 0)
