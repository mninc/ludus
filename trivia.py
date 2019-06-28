import aiohttp
from util.image import centre_image
from textwrap import wrap
from random import shuffle
from html import unescape
import util.number_emotes as numbers
from util.score import won
import asyncio


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
            await centre_image(ctx, ["Categories:", "Do >trivia [category]"] + list(categories.keys()), "scroll_large.png", 27, (0, 0, 0))
            return
        if category and category in categories:
            category = categories[category]
        elif not category:
            category = "15"
        else:
            await centre_image(ctx, ["Invalid category!"], "scroll.png", 40, (0, 0, 0))
            return
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://opentdb.com/api.php?amount=1&category={}&type=multiple".format(category)) as response:
                    r = await response.json()
                    question = r["results"][0]
                    possible_answers = question["incorrect_answers"]
                    possible_answers.append(question["correct_answer"])
                    shuffle(possible_answers)
                    text = wrap(ctx.author.display_name + ":", 20) + wrap(unescape(question["question"]), 20)
                    for wrapped in (wrap(str(i+1) + ": " + unescape(answer), 20) for i, answer in
                                    enumerate(possible_answers)):
                        for string in wrapped:
                            text.append(string)
                    message = await centre_image(ctx, text, "scroll_large.png", 40, (0, 0, 0))
        await message.add_reaction(numbers.one)
        await message.add_reaction(numbers.two)
        await message.add_reaction(numbers.three)
        await message.add_reaction(numbers.four)
        
        def check(emote, user):
            return ctx.author == user and (emote.emoji == numbers.one or emote.emoji == numbers.two
                                           or emote.emoji == numbers.three or emote.emoji == numbers.four)
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=20, check=check)
        except asyncio.TimeoutError:
            await ctx.send(ctx.author.mention + ": Too slow!")
        else:
            correct_answer = possible_answers.index(question["correct_answer"])
            if numbers.numbers.index(reaction.emoji) == correct_answer:
                correct = "That is correct, " + ctx.author.display_name + "!"
                await won(ctx.author, data)
            else:
                correct = "That is incorrect, " + ctx.author.display_name + "."
            text = wrap(correct, 30) + ["The answer was:"] + wrap(str(correct_answer + 1) + ": " +
                                                                  question["correct_answer"], 30)
            await centre_image(ctx, text, "scroll.png", 30, (0, 0, 0))
