def init(bot, data):
    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')
