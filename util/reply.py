import asyncio
import discord


# if user is set, waits for dm from that user instead
# if channel_user is set, waits for messages in ctx's channel from that user
async def get_reply(ctx, timeout, user=None, channel_user=None, any_user=False):
    def check(m):
        if user:
            return isinstance(m.channel, discord.DMChannel) and m.author == user
        elif channel_user:
            return m.author == channel_user and m.channel == ctx.channel
        elif any_user:
            return m.channel == ctx.channel
        else:
            return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await ctx.bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        return
    else:
        return msg
