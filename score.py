from util.score import get_highest


def init(bot, data):
    @bot.command()
    async def score(ctx):
        # display user's score
        if ctx.author.id in data["score"]:
            await ctx.send("Your score is: " + str(data["score"][ctx.author.id]))
        else:
            await ctx.send("Win some games to increase your score!")
    
    @bot.command()
    async def leaderboard(ctx):
        # display top 10 users
        await get_highest(ctx, data)
