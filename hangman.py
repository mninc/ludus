from random import choice
from string import ascii_lowercase
from util.image import send_image
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

print(letter_position)


async def generate_image(ctx, letters):
    return await send_image(ctx, letters, "white.jpg", letter_position, 40, (0, 0, 0))


def update_blank(word, current, character_guess):
    result = ""
    
    for i in range(len(word)):
        if word[i] == character_guess:
            result = result + character_guess  # Adds guess to string if guess is correctly
        
        else:
            # Add the dash at index i to result if it doesn't match the guess
            result = result + current[i]
    
    return result


def init(bot, data):
    @bot.command()
    async def hangman(ctx, user: discord.User = None):
        if user:
            await ctx.send("waiting for response from user")
            await user.send("what word?")
            word = "response"
        else:
            word = choice(words)
        print(word)
        word_displayed = "-" * len(word)
        letters = ascii_lowercase
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        while word_displayed != word:
            print(letters + word_displayed)
            await generate_image(ctx, letters + word_displayed)
            msg = await bot.wait_for('message', check=check)
            content = msg.content
            if len(msg.content) != 1:
                await ctx.send("one character pls")
                continue
            word_displayed = update_blank(word, word_displayed, content)
        await ctx.send("You guessed it! word was " + word)




