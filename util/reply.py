import asyncio
import discord


# if user is set, waits for dm from that user instead
async def get_reply(ctx, timeout, user=None):
    def check(m):
        if user:
            return isinstance(m.channel, discord.DMChannel) and m.author == user
        else:
            return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await ctx.bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        return
    else:
        return msg
