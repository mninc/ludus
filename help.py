import discord


def init(bot, data):
    return
    bot.remove_command("help")
    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title="Help",
                              description="Click [here](https://mninc.github.io/ludus/#commands) to see a list of all the available commands and how to use them!",
                              colour=0xffffff)
        embed.set_image(url="https://mninc.github.io/ludus/img/help.png")
        await ctx.send(embed=embed)
