from random import choice
import asyncio
import util.image as image
from util.reddit import reddit
from textwrap import wrap
from time import time
import util.number_emotes as numbers


def init(bot, data):
    # check wouldyourather is in data, if not we add it
    if "wouldyourather" not in data:
        data["wouldyourather"] = {}
    our_data = data["wouldyourather"]
    
    @bot.command()
    async def wouldyourather(ctx):
        async with ctx.typing():
            threads = list(reddit.subreddit('WouldYouRather').new())
            while True:
                # get random reddit thread
                thread = choice(threads)
                if thread.over_18:  # no nsfw
                    continue
                title = thread.title
                
                if not all(ord(character) < 256 for character in title):  # non-ascii, font will not accept
                    continue
                
                # split title into two options
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
        
        # the title to track it by in the database
        single_title = " or ".join(title) + "?"
        if single_title not in our_data:
            our_data[single_title] = [0, 0]
        
        first = title[0]
        second = title[1]
        text = ["Would you rather:"] + wrap(first, 20) + ["OR"] + wrap(second, 20)
        
        # send message and add reactions
        message = await image.centre_image(ctx, text, "scroll_large.png", 50, (0, 0, 0), 10)
        await message.add_reaction(numbers.one)
        await message.add_reaction(numbers.two)
        await asyncio.sleep(0.1)
        
        def check(emote, user):
            return not user.bot and emote.message.id == message.id and \
                   (emote.emoji == numbers.one or emote.emoji == numbers.two)
        
        start_time = time()
        reacted_users = []
        while time() - start_time < 60:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=5, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                if user.id in reacted_users:  # they have already answered
                    continue
                reacted_users.append(user.id)
                if reaction.emoji == numbers.one:
                    index = 0
                else:
                    index = 1
                
                our_data[single_title][index] += 1
                total = our_data[single_title][0] + our_data[single_title][1]  # total number of people who responded
                percentage = round((our_data[single_title][index] / total) * 100, 2)  # percentage who agreed
                await ctx.send(user.mention + ", " + str(percentage) + "% agreed with you")
