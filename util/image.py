# usage: add 'import util.image as image' to the top of any modules
from PIL import Image, ImageFont, ImageDraw
import discord
import random
import os


async def random_name():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
               "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    name = ""
    for i in range(10):
        name += random.choice(letters)
    return name


# usage:
# ctx is known
# text is an array of text elements ["text1", "text2"]
# path is path of image to load without /images
# location is an array of tuples for each text [(10, 10), (10, 100)]
# font is the font size, in pixels
# colour is a tuple of the rgb
async def send_image(ctx, text, path, loc, size, colour):
    image = Image.open("./images/" + path)
    font = ImageFont.truetype("./res/Roboto-Black.ttf", size)
    d = ImageDraw.Draw(image)

    for i in text:
        text.index(i)
        location = loc[text.index(i)]
        d.text(location, i, font=font, fill=colour)

    pictureDir = "./images/temp" + await random_name() + ".jpg"
    image.save(pictureDir)

    with open(pictureDir, 'rb') as picture:
        message = await ctx.send(file=discord.File(picture, path))
    os.remove(pictureDir)
    return message


# usage:
# same as above, text is an array of text
# offset adds line spacing
async def centre_image(ctx, text, path, size, colour, offset):
    image = Image.open("./images/" + path)
    width, height = image.size
    font = ImageFont.truetype("./res/Roboto-Black.ttf", size)
    d = ImageDraw.Draw(image)

    totalHeight = 0
    for i in text:
        textWidth, textHeight = d.textsize(i)
        totalHeight += textHeight + offset + size

    previousText = 0
    for i in text:
        textWidth, textHeight = d.textsize(i, font=font)
        x = (width-textWidth)/2
        y = (height - totalHeight)/2 + previousText
        d.text((x, y), i, font=font, fill=colour)
        previousText += textHeight + offset

    pictureDir = "./images/temp" + await random_name() + ".jpg"
    image.save(pictureDir)

    with open(pictureDir, 'rb') as picture:
        message = await ctx.send(file=discord.File(picture, path))
    os.remove(pictureDir)
    return message
