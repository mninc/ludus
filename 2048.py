from util.image import add_images
from random import choice, random
from util.score import won
import asyncio


positions = []
x = 0
y = 0
for _ in range(4):
    for _ in range(4):
        positions.append((x, y))
        y += 220
    y = 0
    x += 220

valid = ["2", "4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048"]
emojis = ["⬆", "⬇", "⬅", "➡"]


async def render_board(ctx, board):
    our_positions = []
    numbers = []
    i = 0
    for x in range(4):
        for y in range(4):
            num = board[x][y]
            if num in valid:
                our_positions.append(positions[i])
                numbers.append("2048/" + num + ".png")
            i += 1
    
    return await add_images(ctx, '2048/board.png', numbers, our_positions)


async def add_random(board):
    valid_positions = []
    for x in range(4):
        for y in range(4):
            num = board[x][y]
            if num == "none":
                valid_positions.append((x, y))
    
    if len(valid_positions) == 0:
        return False
    
    position = choice(valid_positions)
    if random() < 0.1:
        board[position[0]][position[1]] = "4"
    else:
        board[position[0]][position[1]] = "2"
    return True


def init(bot, data):
    @bot.command(name="2048")
    async def _2048(ctx):
        board = [["none" for _ in range(4)] for _ in range(4)]
        await add_random(board)
        
        while True:
            message = await render_board(ctx, board)
            for emoji in emojis:
                await message.add_reaction(emoji)
            
            def check(emote, user):
                return not user.bot and ctx.author == user and emote.message.id == message.id and emote.emoji in emojis
            
            try:
                reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send(ctx.author.mention + ": Too slow!")
                return
            else:
                direction = emojis.index(reaction.emoji)
                if direction == 0:
                    for x in range(4):
                        move = True
                        while move:
                            move = False
                            if board[x][2] == "none" and board[x][3] != "none":
                                board[x][2] = board[x][3]
                                board[x][3] = "none"
                                move = True
                            if board[x][1] == "none" and board[x][2] != "none":
                                board[x][1] = board[x][2]
                                board[x][2] = "none"
                                move = True
                            if board[x][0] == "none" and board[x][1] != "none":
                                board[x][0] = board[x][1]
                                board[x][1] = "none"
                                move = True
                            if board[x][3] == board[x][2] != "none":
                                board[x][2] = valid[valid.index(board[x][2]) + 1]
                                board[x][3] = "none"
                                move = True
                            if board[x][2] == board[x][1] != "none":
                                board[x][1] = valid[valid.index(board[x][1]) + 1]
                                board[x][2] = "none"
                                move = True
                            if board[x][1] == board[x][0] != "none":
                                board[x][0] = valid[valid.index(board[x][1]) + 1]
                                board[x][1] = "none"
                                move = True
                elif direction == 1:
                    for x in range(4):
                        move = True
                        while move:
                            move = False
                            if board[x][1] == "none" and board[x][0] != "none":
                                board[x][1] = board[x][0]
                                board[x][0] = "none"
                                move = True
                            if board[x][2] == "none" and board[x][1] != "none":
                                board[x][2] = board[x][1]
                                board[x][1] = "none"
                                move = True
                            if board[x][3] == "none" and board[x][2] != "none":
                                board[x][3] = board[x][2]
                                board[x][2] = "none"
                                move = True
                            if board[x][1] == board[x][0] != "none":
                                board[x][1] = valid[valid.index(board[x][1]) + 1]
                                board[x][0] = "none"
                                move = True
                            if board[x][1] == board[x][2] != "none":
                                board[x][2] = valid[valid.index(board[x][2]) + 1]
                                board[x][1] = "none"
                                move = True
                            if board[x][2] == board[x][3] != "none":
                                board[x][3] = valid[valid.index(board[x][2]) + 1]
                                board[x][2] = "none"
                                move = True
                elif direction == 2:
                    for y in range(4):
                        move = True
                        while move:
                            move = False
                            if board[2][y] == "none" and board[3][y] != "none":
                                board[2][y] = board[3][y]
                                board[3][y] = "none"
                                move = True
                            if board[1][y] == "none" and board[2][y] != "none":
                                board[1][y] = board[2][y]
                                board[2][y] = "none"
                                move = True
                            if board[0][y] == "none" and board[1][y] != "none":
                                board[0][y] = board[1][y]
                                board[1][y] = "none"
                                move = True
                            if board[3][y] == board[2][y] != "none":
                                board[2][y] = valid[valid.index(board[2][y]) + 1]
                                board[3][y] = "none"
                                move = True
                            if board[2][y] == board[1][y] != "none":
                                board[1][y] = valid[valid.index(board[1][y]) + 1]
                                board[2][y] = "none"
                                move = True
                            if board[1][y] == board[0][y] != "none":
                                board[0][y] = valid[valid.index(board[1][y]) + 1]
                                board[1][y] = "none"
                                move = True
                else:
                    for y in range(4):
                        move = True
                        while move:
                            move = False
                            if board[1][y] == "none" and board[0][y] != "none":
                                board[1][y] = board[0][y]
                                board[0][y] = "none"
                                move = True
                            if board[2][y] == "none" and board[1][y] != "none":
                                board[2][y] = board[1][y]
                                board[1][y] = "none"
                                move = True
                            if board[3][y] == "none" and board[2][y] != "none":
                                board[3][y] = board[2][y]
                                board[2][y] = "none"
                                move = True
                            if board[1][y] == board[0][y] != "none":
                                board[1][y] = valid[valid.index(board[1][y]) + 1]
                                board[0][y] = "none"
                                move = True
                            if board[1][y] == board[2][y] != "none":
                                board[2][y] = valid[valid.index(board[2][y]) + 1]
                                board[1][y] = "none"
                                move = True
                            if board[2][y] == board[3][y] != "none":
                                board[3][y] = valid[valid.index(board[2][y]) + 1]
                                board[2][y] = "none"
                                move = True
                
                got_2048 = False
                for x in range(4):
                    for y in range(4):
                        if board[x][y] == "2048":
                            got_2048 = True
                if got_2048:
                    points = await won(ctx.author, data)
                    await ctx.send(ctx.author.mention + ": You beat the game! You got " + str(points) + " points.")
                    return
                if not await add_random(board):
                    await ctx.send(ctx.author.mention + ": You failed. Why not try again?")
                    return
