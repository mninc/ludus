from discord.ext.commands import errors


def init(bot, data):
    @bot.event
    async def on_command_error(ctx, error):
        if type(error) is errors.MissingRequiredArgument:
            await ctx.send(ctx.author.mention +
                           ": You are missing a required argument for this command.\nCheck >help for more information.")
        elif type(error) is errors.CommandNotFound:
            pass
        else:
            await ctx.send(ctx.author.mention + ": An error occurred executing this command. This has been logged.")
            print(error)
