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
# text is the text to be displayed on the image
# path is path of image to load without /images
# name is name of image to be sent to discord
# location is a tuple, x then y
# font is the font size, in pixels
# colour is a tuple of the rgb
# e.g image.send_image(ctx, "cool text", "image.jpg", "image.jpg", (20, 20), 60, (255, 255, 255))
async def send_image(ctx, text, path, name, loc, font, colour):
    image = Image.open("./images/" + path)

    # temp font
    font = ImageFont.truetype("./res/Roboto-Black.ttf", font)
    d = ImageDraw.Draw(image)
    location = (loc[0], loc[1])
    d.text(location, text, font=font, fill=colour)

    pictureDir = "./images/temp" + await random_name() + ".jpg"
    image.save(pictureDir)

    with open(pictureDir, 'rb') as picture:
        await ctx.send(file=discord.File(picture, name))
        await ctx.message.delete()
    os.remove(pictureDir)
