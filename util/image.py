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
    pictureDir = "./images/temp" + await random_name() + ".png"
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
async def centre_image(ctx, text, path, size, colour, send=True, user=False):
    image = Image.open("./images/" + path)
    width, height = image.size
    mid_y = height // 2
    mid_x = width // 2
    font = ImageFont.truetype("./res/font.ttf", size)
    ascent, descent = font.getmetrics()
    font_height = ascent + descent
    d = ImageDraw.Draw(image)
    
    if len(text) % 2 == 0:
        mid_offset = (len(text)//2) * font_height * -1
    else:
        mid_offset = (((len(text) // 2) * font_height) + font_height//2) * -1
    for line in text:
        text_width, _ = d.textsize(line, font=font)
        d.text((mid_x - (text_width // 2), mid_y + mid_offset), line, font=font, fill=colour)
        mid_offset += font_height
    
    if not send:
        return image

    return await post_image(ctx, image, path, user=user)


# image = await send_image(ctx, ['bruh'], 'white.jpg', [(200, 200)], 40, (0, 0, 0), send=False)
# await add_images(ctx, image, ['logo.jpg'], [(0, 0)])
async def add_images(ctx, image, image_paths, locations, send=True, user=False):
    if type(image) is str:
        image = Image.open("./images/" + image)
    
    for i, path in enumerate(image_paths):
        location = locations[i]
        img = Image.open("./images/" + path)
        image.paste(img, location, img)
    
    if not send:
        return image

    return await post_image(ctx, image, 'image.png', user=user)
