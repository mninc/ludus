from util.reply import get_reply
import discord


async def ask_players(ctx, players):
    choices = []
    for num, player in enumerate(players):
        # 3 times to enter either rock paper or scissors
        if num == 0:
            await players[1].send(player.display_name + " is choosing. You will choose after.")
        else:
            await players[0].send(player.display_name + " is choosing. Please wait.")
        for i in range(3):
            await player.send("Please choose either `rock`, `paper` or `scissors` and reply here with one.")
            message = await get_reply(ctx, 30, user=player)
            if message:
                content = message.content.lower()
                if content == "rock" or content == "scissors" or content == "paper":
                    choices.append(content)
                    break
            if i == 2:
                await ctx.send(player.mention + " failed to enter either `rock`, `paper` or `scissors`. What a dummy!")
                return
    return choices


async def send_users(players, text):
    for player in players:
        await player.send(text)


async def check(ctx, choices, players):
    if choices[0] == choices[1]:
        return False
    elif (choices[0] == "rock" and choices[1] == "scissors") or (choices[0] == "paper" and choices[1] == "rock")\
            or (choices[0] == "scissors" and choices[1] == "paper"):
        await ctx.send(players[0].mention + " has won rock, paper, scissors with " + choices[0] + ". " +
                       players[1].mention + " chose " + choices[1] + ".")
        return True
    else:
        await ctx.send(players[1].mention + " has won rock, paper, scissors with " + choices[1] + ". " +
                       players[0].mention + " chose " + choices[0] + ".")
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
                            await send_users(players, "Tie! You bot chose " + choices[0] + ".\nRestarting game.")
                    else:
                        break
