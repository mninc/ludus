from random import choice
from string import ascii_lowercase
from util.image import send_image
from util.reply import get_reply
from util.score import won
import discord
from copy import copy


with open("hangman_words.txt") as f:
    words = f.read().split("\n")

letter_position = []

x = 190
y = 830
for i in range(0, 26):
    if i and not i % 13:
        x = 190
        y += 70
    letter_position.append((x, y))
    x += 50


async def generate_image(ctx, letters, word, lives):
    letter_pos = copy(letter_position)
    y = 110
    if len(word) % 2 == 0:
        x = 500 - ((len(word) // 2) * 40)
    else:
        x = 475 - ((len(word) // 2) * 40)
    for _ in word:
        letter_pos.append((x, y))
        x += 40
    return await send_image(ctx, letters + word, "hangman/hangman" + str(11 - lives) + ".png", letter_pos, 40, (0, 0, 0))


async def update_blank(word, current, character_guess):
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
            if user.bot:
                ctx.send("You can't play against a bot!")
                return
            await ctx.send("Waiting for response from " + user.display_name + "...")
            await user.send("Choose a word for " + ctx.author.display_name + " to guess!")
            reply = await get_reply(ctx, 60, user=user)
            if not reply:
                await ctx.send(user.display_name + " took too long to respond.")
                return
            await user.send("Thank you!")
            word = reply.content
        else:
            word = choice(words)
        word_displayed = "-" * len(word)
        letters = ascii_lowercase
        
        lives = 10
        while word_displayed != word:
            await generate_image(ctx, letters, word_displayed, lives)
            if lives == 0:
                break
            await ctx.send(ctx.author.mention + ": Guess a letter.")
            msg = await get_reply(ctx, 30)
            if not msg:
                await ctx.send(ctx.author.mention + ": You took to long to reply!")
                return
            content = msg.content.lower()
            if len(content) != 1:
                await ctx.send("One character only!")
                continue
            if content not in ascii_lowercase:
                await ctx.send("Invalid character!")
                continue
            if content not in letters:
                await ctx.send("You've already guessed that letter!")
                continue
            
            old_word_displayed = word_displayed
            word_displayed = await update_blank(word, word_displayed, content)
            if word_displayed == old_word_displayed:
                lives -= 1
            letters = letters.replace(content, " ")
        if lives == 0:
            await ctx.send(ctx.author.mention + " you are out of lives! Word was `" + word + "`. Why not try again?")
            return
        score = await won(ctx.author, data)
        await ctx.send(ctx.author.mention + " you guessed it! Word was " + word + ". Your score increased by " +
                       str(score) + ".")
