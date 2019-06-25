from random import choice
from string import ascii_lowercase
from util.image import send_image
from util.reply import get_reply
import discord

with open("hangman_words.txt") as f:
    words = f.read().split("\n")

letter_position = []

# alphabet
x = 100
y = 500
for i in range(0, 26):
    if i and not i % 13:
        x = 100
        y += 40
    letter_position.append((x, y))
    x += 40

# word
x = 100
y = 200
for i in range(0, 40):
    letter_position.append((x, y))
    x += 40


async def generate_image(ctx, letters):
    return await send_image(ctx, letters, "white.jpg", letter_position, 40, (0, 0, 0))


def update_blank(word, current, character_guess):
    result = ""
    for i in range(len(word)):
        if word[i] == character_guess:
            result = result + character_guess
        else:
            result = result + current[i]
    return result


def init(bot, data):
    @bot.command()
    async def hangman(ctx, user: discord.User = None):
        if user:
            await ctx.send("waiting for response from user")
            await user.send("what word?")
            reply = await get_reply(ctx, 60, user=user)
            if not reply:
                await ctx.send("waited too long for response")
                await user.send("timed out")
                return
            word = reply.content
        else:
            word = choice(words)
        print(word)
        word_displayed = "-" * len(word)
        letters = ascii_lowercase
        
        while word_displayed != word:
            old_message = await generate_image(ctx, letters + word_displayed)
            msg = await get_reply(ctx, 30)
            content = msg.content
            if len(msg.content) != 1:
                await ctx.send("one character pls")
                continue
            word_displayed = update_blank(word, word_displayed, content)
            await old_message.delete()
            await msg.delete()
        await ctx.send("You guessed it! word was " + word)




