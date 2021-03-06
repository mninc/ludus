import discord


def init(bot, data):
    @bot.command(aliases=["8ball"])
    async def eightball(ctx, user: discord.User):
        # if a user has been given as an argument, send an image
        if user:
            with open("images/8Ball.png", "rb") as picture:
                await ctx.send(user.mention, file=discord.File(picture, "8ball.png"))
