import discord
import util.reply as reply
import random


def init(bot, data):
    @bot.command()
    async def blackjack(ctx):
        # add image to show black jack start
        await ctx.send("Black Jack started by " + ctx.author.mention + " (high aces).")
        await ctx.send("Type `blackjack join` to join the game (max 5). \n" + ctx.author.mention +
                       " type `start` to begin.\nType `quit` at any point to end the game.")

        players = [ctx.author]
        quitting = False

        for i in range(5):
            answer = await reply.get_reply(ctx, 30, any_user=True)
            if answer.content == "blackjack join" and answer.author not in players:
                players.append(answer.author)
            elif answer.author == ctx.author and answer.content == "start" and len(players) > 1:
                break
            elif answer.author == ctx.author and answer.content == "quit":
                quitting = True
                break
            else:
                await ctx.send("No one joined the game, quitting.")
                quitting = True
                break

        if not quitting:
            text = "The game will now begin with these players: "
            for player in players:
                text += player.mention + ", "
            await ctx.send(text)
            await begin_blackjack(ctx, players)


async def deal_blackjack(players, playerTotals, playedCards, number):
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    async def pick_card():
        while True:
            rank = random.choice(ranks)
            suit = random.choice(suits)
            randomCard = rank + " of " + suit
            imageCard = suit + rank + ".png"
            if randomCard in playedCards:
                continue
            else:
                playedCards.append(randomCard)
                if rank == "King" or rank == "Queen" or rank == "Jack":
                    value = 10
                elif rank == "Ace":
                    value = 11
                else:
                    value = int(rank)

                return randomCard, value, imageCard

    for player in players:
        for i in range(number):
            card, value, image = await pick_card()
            await send_card(player, image)
            playerTotals[player.id]["value"] += value
            playerTotals[player.id]["images"].append(image)


async def send_card(player, path, ctx=None):
    path = "images/cards/" + path
    with open(path, "rb") as picture:
        if ctx:
            await ctx.send(file=discord.File(picture, path))
        else:
            await player.send(file=discord.File(picture, path))


async def send_cards(cards, ctx):
    files = []
    for card in cards:
        path = "images/cards/" + card
        with open(path, "rb") as picture:
            files.append(discord.File(picture, card))
    await ctx.send(files=files)


async def check_bust_blackjack(player, playerTotals):
    if playerTotals[player.id]["value"] > 21:
        playerTotals[player.id]["bust"] = True
        return True
    return False


async def begin_blackjack(ctx, players):
    playerTotals = {}
    playedCards = []
    for player in players:
        playerTotals[player.id] = {"value": 0, "bust": False, "cards": [], "images": []}
    await deal_blackjack(players, playerTotals, playedCards, 2)
    highscore = 0
    topPlayers = []
    for player in players:
        while True:
            await ctx.send(player.mention + " hit or stand?")
            answer = await reply.get_reply(ctx, 30, channel_user=player)
            if answer.content == "stand":
                await ctx.send(player.mention + " is standing.")
                if playerTotals[player.id]["value"] >= highscore:
                    topPlayers = [player.mention]
                    highscore = playerTotals[player.id]["value"]
                break
            if answer.content == "hit":
                await ctx.send("Hitting " + player.mention)
                await deal_blackjack([player], playerTotals, playedCards, 1)
                if await check_bust_blackjack(player, playerTotals):
                    await ctx.send(player.mention + " has gone bust with cards: ")
                    await send_cards(playerTotals[player.id]["images"], ctx)
                    break
            if answer.content == "quit":
                break

    if topPlayers and highscore:
        if len(topPlayers) > 1:
            await ctx.send("The game is finished with top players: " + ", ".join(topPlayers) + " at a score of " + str(highscore) + ".")
        else:
            await ctx.send("The game was won by: " + topPlayers[0] + " at a score of " + str(highscore))

        for player in players:
            await ctx.send(player.mention + " had these cards:")
            await send_cards(playerTotals[player.id]["images"], ctx)
