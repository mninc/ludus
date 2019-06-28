# template file to show how to make files


def init(bot, data):
    @bot.command()
    async def ping(ctx):
        # turn bot.latency (seconds) into ms
        await ctx.send("Pong! Latency: " + str(round(round(bot.latency, 3) * 1000)) + "ms")
