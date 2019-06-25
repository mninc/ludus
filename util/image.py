# usage: add 'import util.image as image' to the top of any modules
from PIL import Image, ImageFont, ImageDraw
import discord
import random
import os
import string


async def random_name():
    name = ""
    for i in range(10):
        name += random.choice(string.ascii_letters)
    return name


# usage:
# ctx is known
# text is an array of text elements ["text1", "text2"]
# path is path of image to load without /images
# location is an array of tuples for each text [(10, 10), (10, 100)]
# font is the font size, in pixels
# colour is a tuple of the rgb
# user is if the message is being sent in the current channel or to the author
async def send_image(ctx, text, path, loc, size, colour, user=False, send=True):
    image = Image.open("./images/" + path)
    font = ImageFont.truetype("./res/Roboto-Black.ttf", size)
    d = ImageDraw.Draw(image)

    for i, text in enumerate(text):
        location = loc[i]
        d.text(location, text, font=font, fill=colour)

    if not send:
        return image

    return await post_image(ctx, image, path, user=user)


async def post_image(ctx, image, path, user=False):
    pictureDir = "./images/temp" + await random_name() + ".jpg"
    image.save(pictureDir)

    with open(pictureDir, 'rb') as picture:
        if user:
            message = await ctx.author.send(file=discord.File(picture, path))
        else:
            message = await ctx.send(file=discord.File(picture, path))
    os.remove(pictureDir)
    return message


# usage:
# same as above, text is an array of text
# offset adds line spacing
async def centre_image(ctx, text, path, size, colour, offset, send=True, user=False):
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
        x = (width - textWidth) / 2
        y = (height - totalHeight) / 2 + previousText
        d.text((x, y), i, font=font, fill=colour)
        previousText += textHeight + offset

    if not send:
        return image

    return await post_image(ctx, image, path, user=user)


# image = await send_image(ctx, ['bruh'], 'white.jpg', [(200, 200)], 40, (0, 0, 0), send=False)
# await add_images(ctx, image, ['logo.jpg'], [(0, 0)])
async def add_images(ctx, image, image_paths, locations, send=True, user=False):
    if type(image) is str:
        image = Image.open(image)

    for i, path in enumerate(image_paths):
        location = locations[i]
        image.paste(Image.open("./images/" + path), location)

    if not send:
        return image

    return await post_image(ctx, image, 'image.jpg', user=user)