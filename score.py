from util.score import get_highest


def init(bot, data):
    @bot.command()
    async def score(ctx):
        if ctx.author.id in data["score"]:
            await ctx.send("Your score is: " + str(data["score"][ctx.author.id]))
        else:
            await ctx.send("Win some games to increase your score!")
    
    @bot.command()
    async def leaderboard(ctx):
        await get_highest(ctx, data)
