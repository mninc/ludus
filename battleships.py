import discord
from util.reply import get_reply
from util.image import add_images
from copy import deepcopy
from util.score import won
from random import choice


# image positions on "real" board (your board)
real_positions = []
x = 115
y = 95
for _ in range(10):
    for _ in range(10):
        real_positions.append((x, y))
        y += 100
    y = 95
    x += 100

# image positions on pegboard (their board)
pegboard_positions = []
x = 120
y = 90
for _ in range(10):
    for _ in range(10):
        pegboard_positions.append((x, y))
        y += 120
    y = 90
    x += 120

blank_board = [["none" for _ in range(10)] for _ in range(10)]
letters = "ABCDEFGHIJ"
ships = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}


async def render_real(user, board):
    our_positions = []
    pieces = []
    rotations = []
    i = 0
    hit_tiles = ["battleships/fire_1.png", "battleships/fire_2.png", "battleships/fire_3.png"]
    for x in range(10):
        for y in range(10):
            ship = board[x][y]
            # work out which image to display, whether to rotate it and whether to put a fire image on top
            if ship != "none" and ship != "miss":
                our_positions.append(real_positions[i])
                if "_hit" in ship:
                    hit = True
                else:
                    hit = False
                ship = ship.replace("_hit", "").replace("_unhit", "")
                if "_h" in ship:
                    rotations.append(90)
                    ship = ship.replace("_h", "")
                else:
                    rotations.append(0)
                    ship = ship.replace("_v", "")
                pieces.append("battleships/" + ship + ".png")
                if hit:
                    our_positions.append(real_positions[i])
                    rotations.append(0)
                    pieces.append(choice(hit_tiles))
            i += 1
    
    return await add_images(user, 'battleships/sea.png', pieces, our_positions, rotations=rotations)


async def render_pegboard(user, board):
    our_positions = []
    pieces = []
    i = 0
    for x in range(10):
        for y in range(10):
            ship = board[x][y]
            # work out which image to display
            if ship == "miss":
                pieces.append("battleships/miss.png")
                our_positions.append(pegboard_positions[i])
            elif "hit" in ship and "unhit" not in ship:
                pieces.append("battleships/hit.png")
                our_positions.append(pegboard_positions[i])
            i += 1
    
    return await add_images(user, 'battleships/pegboard.png', pieces, our_positions,)


async def message_other(player_number, players, message):
    # message the other player
    if player_number:
        await players[0][0].send(message)
    else:
        await players[1][0].send(message)


async def get_xy(string):
    # turn string (eg A4) into x, y co-ordinates
    if len(string) != 2 and len(string) != 3:
        return
    if string[0].upper() not in letters:
        return
    x = letters.index(string[0].upper())
    string = string[1:]
    if not string.isdigit() or not 0 < int(string) <= 10:
        return
    y = int(string) - 1
    return x, y


async def xy_to_string(x, y):
    # turn x, y co-ordinates into a string
    return letters[x] + str(y + 1)


async def get_possible_ship_place_positions(length, position, board):
    # when placing the ships at the start, work out where you can place the end of the ship relative to the starting
    # position
    length -= 1
    possible = []
    if position[0] - length >= 0:
        invalid = False
        for x in range(position[0] - length, position[0]):
            if board[x][position[1]] != "none":
                invalid = True
                break
        if not invalid:
            possible.append(await xy_to_string(position[0] - length, position[1]))
    if position[0] + length <= 9:
        invalid = False
        for x in range(position[0] + 1, position[0] + length + 1):
            if board[x][position[1]] != "none":
                invalid = True
                break
        if not invalid:
            possible.append(await xy_to_string(position[0] + length, position[1]))
    if position[1] - length >= 0:
        invalid = False
        for y in range(position[1] - length, position[1]):
            if board[position[0]][y] != "none":
                invalid = True
                break
        if not invalid:
            possible.append(await xy_to_string(position[0], position[1] - length))
    if position[1] + length <= 9:
        invalid = False
        for y in range(position[1] + 1, position[1] + length + 1):
            if board[position[0]][y] != "none":
                invalid = True
                break
        if not invalid:
            possible.append(await xy_to_string(position[0], position[1] + length))
    return possible


async def add_ship_to_board(start, end, board, ship):
    # using the start and end co-ordinates as well as the ship type to place the ship on the board
    if start[0] == end[0]:
        if start[1] > end[1]:
            temp = end[1]
            end = (end[0], start[1])
            start = (start[0], temp)
        i = 0
        for y in range(start[1], end[1] + 1):
            i += 1
            board[start[0]][y] = ship.lower() + "_" + str(i) + "_v_unhit"
    else:
        if start[0] > end[0]:
            temp = end[0]
            end = (start[0], end[1])
            start = (temp, start[1])
        i = 0
        for x in range(start[0], end[0] + 1):
            i += 1
            board[x][start[1]] = ship.lower() + "_" + str(i) + "_h_unhit"


async def get_other_board(player_number, players):
    # return the other player's board
    if player_number:
        return players[0][1]
    else:
        return players[1][1]


def init(bot, data):
    @bot.command()
    async def battleships(ctx, user: discord.User):
        text = "Battleships - Guess the location of the other player's ships and blow them to smithereens!\n" + \
               user.mention + ": " + ctx.author.display_name + \
               " has invited you to play battleships. Type 'play' to confirm."
        await ctx.send(text)
        
        # wait for the user to confirm
        message = await get_reply(ctx, 30, channel_user=user)
        if not message or message.content.lower() != "play":
            await ctx.send(ctx.author.mention + ": " + user.display_name + " did not confirm.")
            return
        
        players = [[ctx.author, deepcopy(blank_board)], [user, deepcopy(blank_board)]]
        for i, player in enumerate(players):
            user = player[0]
            board = player[1]
            
            await message_other(i, players, user.display_name + " is placing their ships. Please wait.")
            await user.send("Let's place your ships!")
            
            for ship, length in ships.items():
                await render_real(user, board)
                await user.send("Please message the position you want your " + ship + " (length: " + str(length) +
                                ") to start (eg B3)")
                
                # get start position
                while True:
                    position = await get_reply(ctx, 60, user=user)
                    
                    if not position:
                        await user.send("You took too long to reply, the game has been cancelled.")
                        await message_other(i, players, user.display_name +
                                            " took too long to respond. The game has been cancelled.")
                        return
                    
                    position = await get_xy(position.content)
                    if not position:
                        await user.send("That position is invalid. The position must be in the form LetterNumber" +
                                        "eg D6. Try again.")
                        continue
                    if board[position[0]][position[1]] != "none":
                        await user.send("That space is occupied! Try again.")
                        continue
                    break
                
                start_position = position
                possible_next = await get_possible_ship_place_positions(length, position, board)
                await user.send("Where do you want your ship to finish? It must be one of these positions: " +
                                ", ".join(possible_next))
                
                # get end position
                while True:
                    position = await get_reply(ctx, 60, user=user)
                    if not position:
                        await user.send("You took too long to reply, the game has been cancelled.")
                        await message_other(i, players, user.display_name +
                                            " took too long to respond. The game has been cancelled.")
                        return
                    
                    position = position.content
                    if position.upper() not in possible_next:
                        await user.send("That position is invalid. It must be one of these positions: " +
                                        ", ".join(possible_next))
                        continue
                    break
                end_position = await get_xy(position)
                await add_ship_to_board(start_position, end_position, board, ship)
        
        # track how many ship pieces are left for each person to know when they are all sunk
        ship_pieces_left = [17, 17]
        while True:
            for i, player in enumerate(players):
                user = player[0]
                board = player[1]
                
                await message_other(i, players, user.display_name + " is deciding where to attack.")
                
                other_board = await get_other_board(i, players)
                await render_pegboard(user, other_board)
                await render_real(user, board)
                await user.send("Where do you want to attack?")
                
                # get where to attack
                while True:
                    position = await get_reply(ctx, 60, user=user)
                    if not position:
                        await user.send("You took too long to reply, the game has been cancelled.")
                        await message_other(i, players, user.display_name +
                                            " took too long to respond. The game has been cancelled.")
                        return
                    position_str = position.content
                    position = await get_xy(position_str)
                    if not position:
                        await user.send("That position is invalid. The position must be in the form LetterNumber" +
                                        " eg D6. Try again.")
                        continue
                    break
                
                # process shot
                await message_other(i, players, user.display_name + " attacked " + position_str + ".")
                hit = other_board[position[0]][position[1]]
                if "unhit" in hit:
                    other_board[position[0]][position[1]] = hit.replace("unhit", "hit")
                    ship_pieces_left[abs(i - 1)] -= 1
                    await user.send("It's a hit!")
                    await message_other(i, players, "They hit one of your ships.")
                elif "hit" in hit or hit == "miss":
                    await user.send("You already fired there - you wasted a shot.")
                    await message_other(i, players, "They have already shot there.")
                else:
                    other_board[position[0]][position[1]] = "miss"
                    await user.send("It's a miss.")
                    await message_other(i, players, "They missed.")
                
                # show updated board
                await user.send("Updated board:")
                await render_pegboard(user, other_board)
                
                # if the other person has no ships left
                if ship_pieces_left[abs(i - 1)] == 0:
                    score = await won(user, data)
                    await user.send("You have sunk all their ships. You win! Your score increased by " +
                                    str(score) + ".")
                    await message_other(i, players, "They sunk all your ships. They win.")
                    await render_real(players[abs(i - 1)][0], other_board)
                    return
