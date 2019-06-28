import discord
from util.reply import get_reply
from util.image import send_image
import random


class Snake:
    hp = 5

    def __init__(self, player, speed, intimidation, length, scales, damage, hp=None):
        self.user = player
        self.speed = speed
        self.intimidation = intimidation
        self.length = length
        self.scales = scales
        self.damage = damage
        if hp:
            self.hp = hp


async def send_players(players, content):
    for player in players:
        await player.send(content)


async def compare_snakes(ctx, snakes, players, category):
    snake1 = snakes[0]
    snake2 = snakes[1]
    if category == "Speed":
        await send_players(players, "A competition on speed will take place!")
        if snake1.speed == snake2.speed:
            await send_players(players, "Both snakes have equal speeds, no snake is damaged.")
        elif snake1.speed > snake2.speed:
            snake2.hp -= 1
            await send_players(players, snake2.user.name + "'s snake has been damaged, its health is " + str(snake2.hp))
        else:
            snake1.hp -= 1
            await send_players(players, snake1.user.name + "'s snake has been damaged, its health is " + str(snake1.hp))
    elif category == "Intimidation":
        await send_players(players, "The snakes try to intimidate each other!")
        if snake1.intimidation == snake2.intimidation:
            await send_players(players, "Both snakes are equally intimidated, no snake is damaged.")
        elif snake1.intimidation > snake2.intimidation:
            snake2.hp -= 1
            await send_players(players, snake2.user.name + "'s snake has been damaged, its health is " + str(snake2.hp))
        else:
            snake1.hp -= 1
            await send_players(players, snake1.user.name + "'s snake has been damaged, its health is " + str(snake1.hp))
    elif category == "Length":
        await send_players(players, "Which snake is longer?")
        if snake1.length == snake2.length:
            await send_players(players, "Both snakes are equally long, no snake is damaged.")
        elif snake1.length > snake2.length:
            snake2.hp -= 1
            await send_players(players, snake2.user.name + "'s snake has been damaged, its health is " + str(snake2.hp))
        else:
            snake1.hp -= 1
            await send_players(players, snake1.user.name + "'s snake has been damaged, its health is " + str(snake1.hp))
    elif category == "Scales":
        await send_players(players, "The snakes will be judged on their scales.")
        if snake1.scales == snake2.scales:
            await send_players(players, "Both snakes look equally cool, no snake is damaged.")
        elif snake1.scales > snake2.scales:
            snake2.hp -= 1
            await send_players(players, snake2.user.name + "'s snake has been damaged, its health is " + str(snake2.hp))
        else:
            snake1.hp -= 1
            await send_players(players, snake1.user.name + "'s snake has been damaged, its health is " + str(snake1.hp))
    elif category == "Damage":
        await send_players(players, "The snakes will be judged on combat skills. Combat is particularly dangerous, losing will reduce your snake's hp by 2 points.")
        if snake1.damage == snake2.damage:
            await send_players(players, "Both snakes have equal skills, no snake is damaged.")
        elif snake1.damage > snake2.damage:
            if snake2.hp > 1:
                snake2.hp -= 2
            else:
                snake2.hp -= 1
            await send_players(players, snake2.user.name + "'s snake has been damaged, it's health is " + str(snake2.hp))
        else:
            if snake1.hp > 1:
                snake1.hp -= 2
            else:
                snake1.hp -= 1
            await send_players(players, snake1.user.name + "'s snake has been damaged, it's health is " + str(snake1.hp))
    if snake1.hp < 1:
        await send_players(players, snake1.user.name + "'s snake has fallen.")
        await ctx.send(snake2.user.mention + " has won the game!")
        return True
    elif snake2.hp < 1:
        await send_players(players, snake2.user.name + "'s snake has fallen.")
        await ctx.send(snake1.user.mention + " has won the game!")
        return True
    return False


async def send_stats(ctx, snake, players):
    text = [snake.user.name + "'s Snake", "HP: " + str(snake.hp) + "\nSpeed: " + str(snake.speed) + "\nIntimidation: "
            + str(snake.intimidation) + "\nLength: " + str(snake.length) + "\nScales: " + str(snake.scales) +
            "\nDamage: " + str(snake.damage)]
    if snake.user == ctx.author:
        path = "snakes/greencard.png"
    else:
        path = "snakes/orangecard.png"
    await send_image(ctx, text, path, [(90, 32), (30, 470)], 16, (255, 255, 255), dm=players[0])
    await send_image(ctx, text, path, [(90, 32), (30, 470)], 16, (255, 255, 255), dm=players[1])


async def get_points(ctx, player, pointsLeft, category):
    await player.send("**" + category + "**\nPlease enter the number of points to spend on " + category +
                      " *(you have " + str(pointsLeft) + " points remaining)*")
    for i in range(3):
        if pointsLeft == 0:
            return 0
        message = await get_reply(ctx, 25, user=player)
        if message:
            try:
                value = int(message.content)
                if 0 <= value <= pointsLeft:
                    return value
                else:
                    await player.send("Value was not between 0 and the points left to spend.")
            except ValueError:
                await player.send("Value entered was not valid.")
        else:
            await player.send("You took too long to respond.")
            break
    return


async def ask_players(ctx, players, snakes=None):
    newSnakes = []
    # to message player 2
    for num, player in enumerate(players):
        if num == 0:
            await players[1].send(players[0].mention +
                                  " is selecting their stats, you will be able to once they are finished.")
        pointsLeft = 5
        categories = ["Speed", "Intimidation", "Length", "Scales", "Damage"]
        if snakes:
            speed = snakes[num].speed
            intimidation = snakes[num].intimidation
            length = snakes[num].length
            scales = snakes[num].scales
            damage = snakes[num].damage
        else:
            speed = 1
            intimidation = 1
            length = 1
            scales = 1
            damage = 1
        for num1, category in enumerate(categories):
            points = await get_points(ctx, player, pointsLeft, category)
            if points or points == 0:
                pointsLeft -= points
                if num1 == 0:
                    speed += points
                elif num1 == 1:
                    intimidation += points
                elif num1 == 2:
                    length += points
                elif num1 == 3:
                    scales += points
                else:
                    damage += points
            else:
                await send_players(players, player.mention + " has failed to make his snake.")
                return
        if snakes:
            snake = Snake(player, speed, intimidation, length, scales, damage, hp=snakes[num].hp)
            newSnakes.append(snake)
        else:
            snake = Snake(player, speed, intimidation, length, scales, damage)
            newSnakes.append(snake)
        if num == 0:
            await player.send("The next player will now pick their stats.")
    return newSnakes


def init(bot, data):
    @bot.command()
    async def snakes(ctx, user: discord.User):
        if user and not user.bot:
            await ctx.send(user.mention + ": " + ctx.author.display_name +
                           " has invited you to play *snake battles*. Type 'play' to confirm.")
            message = await get_reply(ctx, 30, channel_user=user)
            if not message or message.content.lower() != "play":
                await ctx.send(ctx.author.display_name + ": " + user.display_name + " did not confirm.")
                return
            else:
                players = [ctx.author, user]
                await send_players(players, "Snakes have 5 categories (`speed`, `intimidation`, `length`, `scales` and `damage`). You have 15 points on all categories each round.")
                first = True
                snakes = None
                while True:
                    if first:
                        first = False
                        initSnakes = await ask_players(ctx, players)
                        snakes = initSnakes
                        for snake in snakes:
                            await send_stats(ctx, snake, players)
                        category = random.choice(["Speed", "Intimidation", "Length", "Scales", "Damage"])
                        over = await compare_snakes(ctx, snakes, players, category)
                        if over:
                            break
                        else:
                            await send_players(players, "Both snakes are still alive, select your stats again.")
                    if snakes:
                        newSnakes = await ask_players(ctx, players, snakes=snakes)
                        if not newSnakes:
                            break
                        else:
                            snakes = newSnakes
                        for snake in snakes:
                            await send_stats(ctx, snake, players)
                        category = random.choice(["Speed", "Intimidation", "Length", "Scales", "Damage"])
                        over = await compare_snakes(ctx, snakes, players, category)
                        if over:
                            break
                        else:
                            await send_players(players, "Both snakes are still alive, select your stats again.")
                    else:
                        break
