import discord
from util.image import add_images
from util.reply import get_reply
from random import randint

# positions of counters on background
positions = []
x = 20
y = 19
for _ in range(7):
    for _ in range(6):
        positions.append((x, y))
        y += 99
    y = 19
    x += 99


async def render_board(ctx, board):
    # put pieces on board
    our_positions = []
    counters = []
    i = 0
    for x in range(7):
        for y in range(6):
            counter = board[x][y]
            if counter == "red" or counter == "yellow":
                our_positions.append(positions[i])
            if counter == "red":
                counters.append("connect4/red.png")
            elif counter == "yellow":
                counters.append("connect4/yellow.png")
            i += 1
    
    return await add_images(ctx, 'connect4/board.png', counters, our_positions)


async def check_board_vertical(board):
    # check if there are 4 in a row vertical
    previous_identical = 0
    previous = "none"
    for x in range(7):
        for y in range(6):
            counter = board[x][y]
            if (counter == "yellow" or counter == "red") and previous == counter:
                previous_identical += 1
            else:
                previous_identical = 0
            previous = counter
            if previous_identical == 3:
                return True
        previous_identical = 0
    return False


async def check_board_horizontal(board):
    # check if there are 4 in a row horizontal
    previous_identical = 0
    previous = "none"
    for y in range(6):
        for x in range(7):
            counter = board[x][y]
            if (counter == "yellow" or counter == "red") and previous == counter:
                previous_identical += 1
            else:
                previous_identical = 0
            previous = counter
            if previous_identical == 3:
                return True
        previous_identical = 0
    return False


async def check_board_diagonal(board):
    # check if there are 4 in a row diagonally
    for x in range(7):
        for y in range(6):
            if x + 3 <= 6 and y - 3 >= 0:
                if (board[x][y] == "yellow" or board[x][y] == "red") and board[x][y] == board[x + 1][y - 1] == \
                        board[x + 2][y - 2] == board[x + 3][y - 3]:
                    return True
            if x - 3 >= 0 and y + 3 <= 5:
                if (board[x][y] == "yellow" or board[x][y] == "red") and board[x][y] == board[x - 1][y + 1] == \
                        board[x - 2][y + 2] == board[x - 3][y + 3]:
                    return True
    return False


async def check_board(board):
    # check if there are 4 at all
    if await check_board_vertical(board):
        return True
    elif await check_board_horizontal(board):
        return True
    elif await check_board_diagonal(board):
        return True
    else:
        return False


async def other_player(player, players):
    # get the other player
    if player:
        return players[0]
    else:
        return players[1]


def init(bot, data):
    @bot.command()
    async def connect4(ctx, user: discord.User = None):
        # board with no pieces
        board = [["none" for _ in range(6)] for _ in range(7)]
        
        if user and not user.bot:
            # get other user to confirm
            await ctx.send(user.mention + ": " + ctx.author.display_name +
                           " has invited you to play connect four. Type 'play' to confirm.")
            message = await get_reply(ctx, 30, channel_user=user)
            
            if not message or message.content.lower() != "play":
                await ctx.send(ctx.user + ": " + user.display_name + " did not confirm.")
                return
            
            players = [ctx.author, user]
        else:
            players = [ctx.author, "bot"]
        
        # 0 is yellow, 1 is red
        while True:
            for player_number, player in enumerate(players):
                if player != "bot":
                    # show the board
                    await render_board(ctx, board)
                    await ctx.send(player.mention + ": Pick a column (1-7)")
                    
                    # get the column and check it is valid
                    while True:
                        column = await get_reply(ctx, 20, channel_user=player)
                        if not column:
                            other = await other_player(player_number, players)
                            if other != "bot":
                                await ctx.send(player.display_name + " did not respond.\n" + other.mention +
                                               ": You win!")
                            else:
                                await ctx.send(player.display_name + " did not respond.\nBot wins!")
                            return
                        if len(column.content) == 1 and column.content.isdigit():
                            column = int(column.content) - 1
                            if board[column][0] != "none":
                                await ctx.send(player.mention +
                                               ": That column is full! Please enter a number between 1 and 7.")
                            else:
                                break
                        else:
                            await ctx.send(player.mention + ": That is invalid! Please enter a number between 1 and 7.")
                    
                    # get the y co-ordinate to put the piece
                    previous = 0
                    for y, counter in enumerate(board[column]):
                        if counter != "none":
                            break
                        previous = y
                    
                    if player_number:
                        board[column][previous] = "red"
                    else:
                        board[column][previous] = "yellow"
                else:
                    # get a random column
                    while True:
                        column = randint(0, 6)
                        if board[column][0] == "none":
                            break
                    
                    # get the y co-ordinate
                    previous = 0
                    for y, counter in enumerate(board[column]):
                        if counter != "none":
                            break
                        previous = y
                    
                    if player_number:
                        board[column][previous] = "red"
                    else:
                        board[column][previous] = "yellow"
                
                # see if there is a winner
                winner = await check_board(board)
                if winner:
                    if player == "bot":
                        await render_board(ctx, board)
                        await ctx.send("Bot wins!")
                    else:
                        await render_board(ctx, board)
                        await ctx.send(player.mention + ": You won!")
                    return
