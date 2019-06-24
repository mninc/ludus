# .____              .___
# |    |    __ __  __| _/_ __  ______
# |    |   |  |  \/ __ |  |  \/  ___/
# |    |___|  |  / /_/ |  |  /\___ \
# |_______ \____/\____ |____//____  >
#         \/          \/          \/


def init(bot, data):
    @bot.command()
    async def textadv(ctx, *args):
        if args[0] == "begin":
            await begin(ctx)
        else:
            pass


# function run on /textadv begin
async def begin(ctx):
    user = ctx.message.author
    await user.send("begin game")
