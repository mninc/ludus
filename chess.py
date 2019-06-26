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
        await ctx.send(user.mention + ": " + ctx.author.display_name +
                       " has invited you to play chess. Type 'play' to confirm.")
        message = await get_reply(ctx, 30, channel_user=user)
        if not message or message.content.lower() != "play":
            await ctx.send(ctx.user + ": " + user.display_name + " did not confirm.")
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
        while True:
            for player_number, player in enumerate(players):
                await render_board(ctx, board)
                await ctx.send(player.mention +
                               ": Your move! Write the tile to move a chess piece from and to, eg B1 C3")
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
                    first_y = int(first[1]) - 1
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
                    second_y = int(second[1]) - 1
                    
                    
                    
