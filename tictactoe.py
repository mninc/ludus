import discord
from util.reply import get_reply
from util.image import add_images
from copy import deepcopy
from util.score import won


positions = []
x = 61
y = 61
for _ in range(3):
    for _ in range(3):
        positions.append((x, y))
        y += 60
    y = 61
    x += 60
blank_board = [["none" for _ in range(3)] for _ in range(3)]
letters = "ABC"


async def render_board(ctx, board):
    our_positions = []
    pieces = []
    i = 0
    for x in range(3):
        for y in range(3):
            square = board[x][y]
            if square != "none":
                our_positions.append(positions[i])
                pieces.append(square + ".png")
            i += 1
    
    return await add_images(ctx, 'tictactoe.png', pieces, our_positions)


async def get_xy(string):
    if len(string) != 2:
        return
    if string[0].upper() not in letters:
        return
    x = letters.index(string[0].upper())
    if not string[1].isdigit() or not 0 < int(string[1]) <= 3:
        return
    y = int(string[1]) - 1
    return x, y


async def check_winner(board):
    for x in range(3):
        if board[x][0] == board[x][1] == board[x][2] != "none":
            return True
    for y in range(3):
        if board[0][y] == board[1][y] == board[2][y] != "none":
            return True
    if board[0][0] == board[1][1] == board[2][2] != "none":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "none":
        return True
    return False


async def check_draw(board):
    for x in range(3):
        for y in range(3):
            if board[x][y] == "none":
                return False
    return True


def init(bot, data):
    @bot.command(aliases=["ttt", "tic_tac_toe"])
    async def tictactoe(ctx, user: discord.User):
        if user.bot:
            await ctx.send("You can't play against a bot! Unless they're a selfbot.")
            return
        text = "Tic tac toe!\n" + user.mention + ": " + ctx.author.display_name + \
               " has invited you to play tic tac toe. Type 'play' to confirm."
        await ctx.send(text)
        message = await get_reply(ctx, 30, channel_user=user)
        if not message or message.content.lower() != "play":
            await ctx.send(ctx.author.mention + ": " + user.display_name + " did not confirm.")
            return
        
        board = deepcopy(blank_board)
        
        players = [ctx.author, user]
        
        while True:
            for i, player in enumerate(players):
                await render_board(ctx, board)
                text = player.mention + ": Pick a square to place a "
                if i:
                    text += "nought."
                else:
                    text += "cross."
                await ctx.send(text)
                while True:
                    position = await get_reply(ctx, 30, channel_user=player)
                    if not position:
                        await ctx.send("You took too long to reply, the game has been cancelled.")
                        return
                    position = await get_xy(position.content)
                    if not position:
                        await ctx.send("That position is invalid. The position must be in the form LetterNumber" +
                                       " eg D6. Try again.")
                        continue
                    if board[position[0]][position[1]] != "none":
                        await ctx.send("That space is occupied! Try again.")
                        continue
                    break
                if i:
                    board[position[0]][position[1]] = "nought"
                else:
                    board[position[0]][position[1]] = "cross"
                
                if await check_winner(board):
                    await render_board(ctx, board)
                    score = await won(player, data)
                    await ctx.send("GG! " + player.mention + " wins! Their score increased by " + str(score) + ".")
                    return
                elif await check_draw(board):
                    await render_board(ctx, board)
                    await ctx.send("It's a draw. Why not play again?")
                    return
