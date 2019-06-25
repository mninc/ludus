import discord
from util.image import add_images
from util.reply import get_reply


def init(bot, data):
    @bot.command()
    async def connect4(ctx, user: discord.User = None):
        await add_images(ctx, 'white.jpg', ['connect4_counter_red.png', 'connect4_counter_yellow.png'], [(0, 0), (100, 100)])
        if user:
            await ctx.send(user.mention + ": " + ctx.author.display_name + " has invited you to play connect four. Type 'play' to confirm")
            # reply from user in ctx channel
            # message = get_reply(ctx, 30)
            if not message or message.content.lower() != "play":
                await ctx.send("user did not confirm")
                return
            players = [ctx.user, "us"]
        else:
            players = [ctx.user, user]
        
        while True:
            for player in players:
                pass
        
            

