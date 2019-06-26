import aiohttp
from util.image import centre_image
from textwrap import wrap
from random import shuffle
from html import unescape
import util.number_emotes as numbers
import asyncio


def init(bot, data):
    @bot.command()
    async def trivia(ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://opentdb.com/api.php?amount=1&category=15&type=multiple") as response:
                    r = await response.json()
                    question = r["results"][0]
                    possible_answers = question["incorrect_answers"]
                    possible_answers.append(question["correct_answer"])
                    shuffle(possible_answers)
                    text = wrap(ctx.author.display_name + ":", 20) + wrap(unescape(question["question"]), 20)
                    for wrapped in (wrap(str(i+1) + ": " + unescape(answer), 20) for i, answer in enumerate(possible_answers)):
                        for string in wrapped:
                            text.append(string)
                    message = await centre_image(ctx, text, "scroll_large.png", 40, (0, 0, 0), 15)
                    print(question["correct_answer"])
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
                        else:
                            correct = "That is incorrect, " + ctx.author.display_name + "."
                        text = wrap(correct, 30) + ["The answer was:"] + wrap(str(correct_answer + 1) + ": " +
                                                                              question["correct_answer"], 30)
                        await centre_image(ctx, text, "scroll.png", 30, (0, 0, 0), 15)
