def init(bot, data):
    @bot.command()
    async def ping(ctx):
        print(ctx.message.content)
        await ctx.send('pong')

