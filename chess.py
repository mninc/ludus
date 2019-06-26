import discord
from util.reply import get_reply
from util.image import add_images


letters = "ABCDEFGH"

positions = []
x = 40
y = 40
for _ in range(8):
    for _ in range(8):
        positions.append((x + 11, y + 11))
        y += 22
    y = 40
    x += 22


async def render_board(ctx, board):
    our_positions = []
    pieces = []
    i = 0
    for x in range(8):
        for y in range(8):
            counter = board[x][y]
            if counter != "none":
                our_positions.append(positions[i])
            if counter == "b_rook":
                pieces.append("black_rook.png")
            elif counter == "b_knight":
                pieces.append("black_knight.png")
            elif counter == "b_bishop":
                pieces.append("black_bishop.png")
            elif counter == "b_queen":
                pieces.append("black_queen.png")
            elif counter == "b_king":
                pieces.append("black_king.png")
            elif counter == "b_pawn":
                pieces.append("black_pawn.png")
            if counter == "w_rook":
                pieces.append("white_rook.png")
            elif counter == "w_knight":
                pieces.append("white_knight.png")
            elif counter == "w_bishop":
                pieces.append("white_bishop.png")
            elif counter == "w_queen":
                pieces.append("white_queen.png")
            elif counter == "w_king":
                pieces.append("white_king.png")
            elif counter == "w_pawn":
                pieces.append("white_pawn.png")
            i += 1
    
    return await add_images(ctx, 'chessboard.png', pieces, our_positions, centre=True)


async def other_player(player, players):
    if player:
        return players[0]
    else:
        return players[1]


def init(bot, data):
    @bot.command()
    async def chess(ctx, user: discord.User):
        text = "Chess with a twist! No check or checkmate, just take your opponent's king.\n" + user.mention + ": " + \
               ctx.author.display_name + " has invited you to play chess. Type 'play' to confirm."
        await ctx.send(text)
        message = await get_reply(ctx, 30, channel_user=user)
        if not message or message.content.lower() != "play":
            await ctx.send(ctx.author.mention + ": " + user.display_name + " did not confirm.")
            return
        
        players = [ctx.author, user]
        board = [
            ["b_rook", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_rook"],
            ["b_knight", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_knight"],
            ["b_bishop", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_bishop"],
            ["b_queen", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_queen"],
            ["b_king", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_king"],
            ["b_bishop", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_bishop"],
            ["b_knight", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_knight"],
            ["b_rook", "b_pawn", "none", "none", "none", "none", "w_pawn", "w_rook"]
        ]
        
        # 0 is white, 1 is black
        checkmate = False
        while not checkmate:
            for player_number, player in enumerate(players):
                if checkmate:
                    break
                await render_board(ctx, board)
                text = player.mention + ": Your move!"
                if player_number:
                    text += " You are black. "
                else:
                    text += " You are white. "
                text += "Write the tile to move a chess piece from and to, eg B1 C3"
                await ctx.send(text)
                while True:
                    move = await get_reply(ctx, 120, channel_user=player)
                    if not move:
                        other = await other_player(player_number, players)
                        await ctx.send(other.mention + ": " + player.display_name + " failed to respond. You win!")
                        return
                    move = move.content.split(" ")
                    if len(move) != 2:
                        await ctx.send(player.mention + ": Please enter two tiles.")
                        continue
                    first = move[0].upper()
                    if len(first) != 2 or first[0] not in letters or not first[1].isdigit() or \
                            not 0 < int(first[1]) <= 8:
                        await ctx.send(player.mention + ": Invalid tile!")
                        continue
                    first_x = letters.index(first[0])
                    first_y = 8 - int(first[1])
                    if player_number:
                        if not board[first_x][first_y].startswith("b_"):
                            await ctx.send(player.mention + ": You do not have a piece on this tile.")
                            continue
                    else:
                        if not board[first_x][first_y].startswith("w_"):
                            await ctx.send(player.mention + ": You do not have a piece on this tile.")
                            continue
                    second = move[1].upper()
                    if len(second) != 2 or second[0] not in letters or not second[1].isdigit() or \
                            not 0 < int(second[1]) <= 8:
                        await ctx.send(player.mention + ": Invalid tile!")
                        continue
                    second_x = letters.index(second[0])
                    second_y = 8 - int(second[1])
                    
                    piece = board[first_x][first_y][2:]
                    
                    if piece == "pawn":
                        if player_number:
                            if second_y != first_y + 1:
                                if first_y == 1:
                                    if second_y != first_y + 2:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                else:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                            if first_x == second_x:
                                if second_y == first_y + 2:
                                    if board[first_x][first_y + 1] != "none" or board[first_x][first_y + 2] != "none":
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    else:
                                        board[first_x][first_y] = "none"
                                        board[second_x][second_y] = "b_pawn"
                                        break
                                else:
                                    if board[first_x][first_y + 1] != "none":
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    else:
                                        board[first_x][first_y] = "none"
                                        board[second_x][second_y] = "b_pawn"
                                        if second_y == 7:
                                            new_pieces = ["bishop", "knight", "queen", "rook", "pawn"]
                                            await ctx.send(player.mention +
                                                           ": What will you convert your pawn to? Choose one of " +
                                                           ", ".join(new_pieces[:-1]) + " or " +
                                                           new_pieces[len(new_pieces) - 1])
                                            while True:
                                                new_piece = await get_reply(ctx, 120, channel_user=player)
                                                if not new_piece:
                                                    other = await other_player(player_number, players)
                                                    await ctx.send(other.mention + ": " + player.display_name +
                                                                   " failed to respond. You win!")
                                                    return
                                                new_piece = new_piece.content.lower()
                                                if new_piece not in new_pieces:
                                                    await ctx.send(player.mention + ": Invalid piece. Pick again.")
                                                    continue
                                                break
                                            board[second_x][second_y] = "b_" + new_piece
                            else:
                                if second_x != first_x + 1 and second_x != first_x - 1:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if not board[second_x][second_y].startswith("w_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "b_pawn"
                                if second_y == 7:
                                    new_pieces = ["bishop", "knight", "queen", "rook", "pawn"]
                                    await ctx.send(player.mention +
                                                   ": What will you convert your pawn to? Choose one of " +
                                                   ", ".join(new_pieces[:-1]) + " or " +
                                                   new_pieces[len(new_pieces) - 1])
                                    while True:
                                        new_piece = await get_reply(ctx, 120, channel_user=player)
                                        if not new_piece:
                                            other = await other_player(player_number, players)
                                            await ctx.send(other.mention + ": " + player.display_name +
                                                           " failed to respond. You win!")
                                            return
                                        new_piece = new_piece.content.lower()
                                        if new_piece not in new_pieces:
                                            await ctx.send(player.mention + ": Invalid piece. Pick again.")
                                            continue
                                        break
                                    board[second_x][second_y] = "b_" + new_piece
                        else:
                            if second_y != first_y - 1:
                                if first_y == 6:
                                    if second_y != first_y - 2:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                else:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                            if first_x == second_x:
                                if second_y == first_y - 2:
                                    if board[first_x][first_y - 1] != "none" or board[first_x][first_y - 2] != "none":
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    else:
                                        board[first_x][first_y] = "none"
                                        board[second_x][second_y] = "w_pawn"
                                else:
                                    if board[first_x][first_y - 1] != "none":
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    else:
                                        board[first_x][first_y] = "none"
                                        board[second_x][second_y] = "w_pawn"
                                        if second_y == 0:
                                            new_pieces = ["bishop", "knight", "queen", "rook", "pawn"]
                                            await ctx.send(player.mention +
                                                           ": What will you convert your pawn to? Choose one of " +
                                                           ", ".join(new_pieces[:-1]) + " or " +
                                                           new_pieces[len(new_pieces) - 1])
                                            while True:
                                                new_piece = await get_reply(ctx, 120, channel_user=player)
                                                if not new_piece:
                                                    other = await other_player(player_number, players)
                                                    await ctx.send(other.mention + ": " + player.display_name +
                                                                   " failed to respond. You win!")
                                                    return
                                                new_piece = new_piece.content.lower()
                                                if new_piece not in new_pieces:
                                                    await ctx.send(player.mention + ": Invalid piece. Pick again.")
                                                    continue
                                                break
                                            board[second_x][second_y] = "w_" + new_piece
                            else:
                                if second_x != first_x - 1 and second_x != first_x + 1:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if not board[second_x][second_y].startswith("b_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "w_pawn"
                                if second_y == 0:
                                    new_pieces = ["bishop", "knight", "queen", "rook", "pawn"]
                                    await ctx.send(player.mention +
                                                   ": What will you convert your pawn to? Choose one of " +
                                                   ", ".join(new_pieces[:-1]) + " or " +
                                                   new_pieces[len(new_pieces) - 1])
                                    while True:
                                        new_piece = await get_reply(ctx, 120, channel_user=player)
                                        if not new_piece:
                                            other = await other_player(player_number, players)
                                            await ctx.send(other.mention + ": " + player.display_name +
                                                           " failed to respond. You win!")
                                            return
                                        new_piece = new_piece.content.lower()
                                        if new_piece not in new_pieces:
                                            await ctx.send(player.mention + ": Invalid piece. Pick again.")
                                            continue
                                        break
                                    board[second_x][second_y] = "w_" + new_piece
                    elif piece == "rook":
                        if player_number:
                            if first_x != second_x and first_y != second_y:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if first_x == second_x:
                                invalid = False
                                start = True
                                for i in range(first_y, second_y):
                                    if start:
                                        start = False
                                        continue
                                    if board[first_x][i] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("b_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "b_rook"
                            else:
                                invalid = False
                                start = True
                                for i in range(first_x, second_x):
                                    if start:
                                        start = False
                                        continue
                                    if board[i][first_y] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("b_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "b_rook"
                        else:
                            if first_x != second_x and first_y != second_y:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if first_x == second_x:
                                invalid = False
                                start = True
                                for i in range(first_y, second_y):
                                    if start:
                                        start = False
                                        continue
                                    if board[first_x][i] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("w_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "w_rook"
                            else:
                                invalid = False
                                start = True
                                for i in range(first_x, second_x):
                                    if start:
                                        start = False
                                        continue
                                    if board[i][first_y] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("w_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "w_rook"
                    elif piece == "bishop":
                        if player_number:
                            if abs(first_x - second_x) != abs(first_y - second_y):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            invalid = False
                            start = True
                            for i, j in zip(range(first_x, second_x), range(first_y, second_y)):
                                if start:
                                    start = False
                                    continue
                                if board[i][j] != "none":
                                    invalid = True
                                    break
                            if invalid:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if board[second_x][second_y].startswith("b_"):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            board[first_x][first_y] = "none"
                            board[second_x][second_y] = "b_bishop"
                        else:
                            if abs(first_x - second_x) != abs(first_y - second_y):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            invalid = False
                            start = True
                            for i, j in zip(range(first_x, second_x), range(first_y, second_y)):
                                if start:
                                    start = False
                                    continue
                                if board[i][j] != "none":
                                    invalid = True
                                    break
                            if invalid:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if board[second_x][second_y].startswith("w_"):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            board[first_x][first_y] = "none"
                            board[second_x][second_y] = "w_bishop"
                    elif piece == "queen":
                        if player_number:
                            if first_x == second_x or first_y == second_y:
                                if first_x == second_x:
                                    invalid = False
                                    start = True
                                    for i in range(first_y, second_y):
                                        if start:
                                            start = False
                                            continue
                                        if board[first_x][i] != "none":
                                            invalid = True
                                            break
                                    if invalid:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    if board[second_x][second_y].startswith("b_"):
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    board[first_x][first_y] = "none"
                                    board[second_x][second_y] = "b_queen"
                                else:
                                    invalid = False
                                    start = True
                                    for i in range(first_x, second_x):
                                        if start:
                                            start = False
                                            continue
                                        if board[i][first_y] != "none":
                                            invalid = True
                                            break
                                    if invalid:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    if board[second_x][second_y].startswith("b_"):
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    board[first_x][first_y] = "none"
                                    board[second_x][second_y] = "b_queen"
                            else:
                                if abs(first_x - second_x) != abs(first_y - second_y):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                invalid = False
                                start = True
                                for i, j in zip(range(first_x, second_x), range(first_y, second_y)):
                                    if start:
                                        start = False
                                        continue
                                    if board[i][j] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("b_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "b_queen"
                        else:
                            if first_x == second_x or first_y == second_y:
                                if first_x == second_x:
                                    invalid = False
                                    start = True
                                    for i in range(first_y, second_y):
                                        if start:
                                            start = False
                                            continue
                                        if board[first_x][i] != "none":
                                            invalid = True
                                            break
                                    if invalid:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    if board[second_x][second_y].startswith("w_"):
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    board[first_x][first_y] = "none"
                                    board[second_x][second_y] = "w_queen"
                                else:
                                    invalid = False
                                    start = True
                                    for i in range(first_x, second_x):
                                        if start:
                                            start = False
                                            continue
                                        if board[i][first_y] != "none":
                                            invalid = True
                                            break
                                    if invalid:
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    if board[second_x][second_y].startswith("w_"):
                                        await ctx.send(player.mention + ": Invalid move!")
                                        continue
                                    board[first_x][first_y] = "none"
                                    board[second_x][second_y] = "w_queen"
                            else:
                                if abs(first_x - second_x) != abs(first_y - second_y):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                invalid = False
                                start = True
                                for i, j in zip(range(first_x, second_x), range(first_y, second_y)):
                                    if start:
                                        start = False
                                        continue
                                    if board[i][j] != "none":
                                        invalid = True
                                        break
                                if invalid:
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                if board[second_x][second_y].startswith("w_"):
                                    await ctx.send(player.mention + ": Invalid move!")
                                    continue
                                board[first_x][first_y] = "none"
                                board[second_x][second_y] = "w_queen"
                    elif piece == "king":
                        if player_number:
                            if abs(first_x - second_x) > 1 or abs(first_y - second_y) > 1:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if board[second_x][second_y].startswith("b_"):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            board[first_x][first_y] = "none"
                            board[second_x][second_y] = "b_king"
                        else:
                            if abs(first_x - second_x) > 1 or abs(first_y - second_y) > 1:
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            if board[second_x][second_y].startswith("w_"):
                                await ctx.send(player.mention + ": Invalid move!")
                                continue
                            board[first_x][first_y] = "none"
                            board[second_x][second_y] = "w_king"
                    
                    found_king = False
                    for x in range(8):
                        for y in range(8):
                            if player_number and board[x][y] == "w_king":
                                found_king = True
                            elif not player_number and board[x][y] == "b_king":
                                found_king = True
                    if not found_king:
                        await render_board(ctx, board)
                        await ctx.send("GG! " + player.mention + " wins!")
                        checkmate = True
                    break
