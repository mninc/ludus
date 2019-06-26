from util.reply import get_reply
import discord


async def ask_players(ctx, players):
    choices = []
    for num, player in enumerate(players):
        # 3 times to enter either rock paper or scissors
        for i in range(3):
            await player.send("Please choose either `rock`, `paper` or `scissors` and reply here with one.")
            message = await get_reply(ctx, 30, user=player)
            if message:
                if message.content == "rock" or message.content == "scissors" or message.content == "paper":
                    choices.append(message.content)
                    break
            if i == "2" and not choices[num]:
                await ctx.send(player.mention + " failed to enter either `rock`, `paper` or `scissors`.")
                return
    return choices


async def check(ctx, choices, players):
    if choices[0] == choices[1]:
        await ctx.send("Tie, both " + players[0].mention + " and " + players[1].mention + " chose " + choices[0])
        return False
    elif (choices[0] == "rock" and choices[1] == "scissors") or (choices[0] == "paper" and choices[1] == "rock")\
            or (choices[0] == "scissors" and choices[1] == "paper"):
        await ctx.send(players[0].mention + " has won with " + choices[0])
        return True
    else:
        await ctx.send(players[1].mention + " has won with " + choices[1])
        return True


def init(bot, data):
    @bot.command(aliases=["rockpaperscissors"])
    async def rps(ctx, user: discord.User):
        if user and not user.bot:
            await ctx.send(user.mention + ": " + ctx.author.display_name +
                           " has invited you to play rock paper scissors. Type 'play' to confirm.")
            message = await get_reply(ctx, 30, channel_user=user)
            if not message or message.content.lower() != "play":
                await ctx.send(ctx.user + ": " + user.display_name + " did not confirm.")
                return
            else:
                while True:
                    players = [ctx.author, user]
                    choices = await ask_players(ctx, players)
                    if choices:
                        finished = await check(ctx, choices, players)
                        if finished:
                            break
                        else:
                            await ctx.send("Restarting the game.")
                    else:
                        break
