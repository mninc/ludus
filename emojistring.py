from string import ascii_lowercase


def init(bot, data):
    @bot.command()
    async def emojistring(ctx, *args):
        text = " ".join(args)
        message = ""
        for char in text:
            if char.lower() in ascii_lowercase:
                message += ":regional_indicator_" + char.lower() + ":"
            else:
                message += char
        await ctx.send(message)
