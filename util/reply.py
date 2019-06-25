import asyncio


# dm for if the message being awaited is DM or not
def get_reply(ctx, timeout):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await ctx.bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        return
    else:
        return msg
