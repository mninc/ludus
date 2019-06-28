import aiohttp
from util.image import centre_image
from textwrap import wrap
from random import shuffle
from html import unescape
import util.number_emotes as numbers
from util.score import won
import asyncio


# valid categories for the opentdb api
categories = {
    "general knowledge": "9",
    "books": "10",
    "film": "11",
    "music": "12",
    "musicals and theatre": "13",
    "television": "14",
    "video games": "15",
    "board games": "16",
    "science and nature": "17",
    "computers": "18",
    "mathematics": "19",
    "mythology": "20",
    "sports": "21",
    "geography": "22",
    "history": "23",
    "politics": "24",
    "art": "25",
    "celebrities": "26",
    "animals": "27",
    "vehicles": "28"
}


def init(bot, data):
    @bot.command()
    async def trivia(ctx, *args):
        category = " ".join(args).lower()
        if category and category == "categories":
            # display categories
            await centre_image(ctx, ["Categories:", "Do >trivia [category]"] + list(categories.keys()), "scroll_large.png", 27, (0, 0, 0))
            return
        
        # check category is valid
        if category and category in categories:
            category = categories[category]
        elif not category:  # no category specified, use default
            category = "15"
        else:
            await centre_image(ctx, ["Invalid category!"], "scroll.png", 40, (0, 0, 0))
            return
        
        async with ctx.typing():
            # get response from api
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://opentdb.com/api.php?amount=1&category={}&type=multiple".format(category)) as response:
                    r = await response.json()
                    question = r["results"][0]
                    
                    # get all the answers, incorrect and correct, and shuffle them
                    possible_answers = question["incorrect_answers"]
                    possible_answers.append(question["correct_answer"])
                    shuffle(possible_answers)
                    
                    # display trivia
                    text = wrap(ctx.author.display_name + ":", 20) + wrap(unescape(question["question"]), 20)
                    for wrapped in (wrap(str(i+1) + ": " + unescape(answer), 20) for i, answer in
                                    enumerate(possible_answers)):
                        for string in wrapped:
                            text.append(string)
                    message = await centre_image(ctx, text, "scroll_large.png", 40, (0, 0, 0))
        
        # add reactions
        await message.add_reaction(numbers.one)
        await message.add_reaction(numbers.two)
        await message.add_reaction(numbers.three)
        await message.add_reaction(numbers.four)
        
        def check(emote, user):
            # check the user is not a bot, the reaction is on the right message, the user is the user who started the
            # command and that the reaction is 1, 2, 3 or 4
            return not user.bot and emote.message.id == message.id and ctx.author == user and \
                   emote.emoji in numbers.numbers
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=20, check=check)
        except asyncio.TimeoutError:
            # took too long to react
            await ctx.send(ctx.author.mention + ": Too slow!")
        else:
            correct_answer = possible_answers.index(question["correct_answer"])
            if numbers.numbers.index(reaction.emoji) == correct_answer:  # they got it right
                correct = "That is correct, " + ctx.author.display_name + "!"
                await won(ctx.author, data)  # they get points, but they aren't told this
            else:  # they got it wrong
                correct = "That is incorrect, " + ctx.author.display_name + "."
            text = wrap(correct, 30) + ["The answer was:"] + wrap(str(correct_answer + 1) + ": " +
                                                                  question["correct_answer"], 30)
            
            await centre_image(ctx, text, "scroll.png", 30, (0, 0, 0))
