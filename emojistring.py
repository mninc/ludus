from string import ascii_lowercase


def init(bot, data):
    @bot.command(aliases=["emojitext"])
    async def emojistring(ctx, *args):
        text = " ".join(args)
        message = ""
        for char in text:
            if char.lower() in ascii_lowercase:
                message += ":regional_indicator_" + char.lower() + ":"
            else:
                message += char
        await ctx.send(message)
        await ctx.message.delete()
