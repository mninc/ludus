def init(bot, data):
    @bot.command()
    async def ping(ctx):
        await ctx.send("Pong! Latency: " + str(round(round(bot.latency, 3) * 1000)) + "ms")
