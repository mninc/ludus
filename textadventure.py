# .____              .___
# |    |    __ __  __| _/_ __  ______
# |    |   |  |  \/ __ |  |  \/  ___/
# |    |___|  |  / /_/ |  |  /\___ \
# |_______ \____/\____ |____//____  >
#         \/          \/          \/
import util.reply as reply
import util.image as image
import json


class Player:
    alive = True
    roundID = "1"
    inventory = []

    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.damage = 1

    async def set_name(self, new_name):
        self.name = new_name

    async def die(self):
        self.alive = False

    async def set_scene(self, new_scene):
        self.roundID = new_scene

    async def set_damage(self, new_damage):
        self.damage = new_damage

    async def add_inv(self, item):
        self.inventory.append(item)


def load_file_text(path):
    with open("res/" + path, "r") as file:
        return file.read()


def load_file_json(path):
    with open("res/" + path) as file:
        return json.load(file)


def init(bot, data):
    introText = load_file_text("intro.txt")
    choices = load_file_json("choices.json")

    @bot.command()
    async def adventure(ctx):
        await begin(ctx)

    # function run on /textadv begin
    async def begin(ctx):
        user = ctx.message.author
        await user.send("Hello " + user.name + " " + introText)
        player = Player(user.name, user)
        await story(ctx, player, choices)


# function with main game loop
async def story(ctx, player, choices):
    alive = player.alive
    while alive:
        options = choices[player.roundID]["options"]

        options = await inventory_check(player, options)

        if "death" in options:
            await process_image(ctx, choices, player, death=True)
            break
        else:
            await process_image(ctx, choices, player)

        answer = await reply.get_reply(ctx, 60, player.user)
        if answer:
            answer = answer.content
            if len(options) == 1 and answer == "1":
                await player.set_scene(options[0])
            elif answer == "1" or answer == "2" or answer == "3":
                answer = int(answer)
                await player.set_scene(options[answer - 1])
            elif answer == "inventory":
                await display_inventory(ctx, player)
            elif answer == "quit":
                await player.user.send("Game over.")
                break
        else:
            await player.user.send("You were inactive for too long, quitting.")
            break


async def display_inventory(ctx, player):
    if player.inventory:
        imageText = ["Inventory:", "These are the items you have gathered:"] + player.inventory
    else:
        imageText = ["Inventory:", "You haven't found any items."]
    await image.centre_image(ctx, imageText, "black.jpg", 15, (255, 255, 255), True, player.user)


# checks if there is anything to add to the inventory from the options
async def inventory_check(player, options):
    possibleItems = ["snake"]
    itemDescriptions = ["A very cool snake"]
    for num, item in enumerate(possibleItems):
        if item in options:
            await player.add_inv("- " + itemDescriptions[num])
            await player.user.send("*" + itemDescriptions[num] + "* has been added to your inventory.")
            options = options.pop(num)
    return options


# interacts with util.image to avoid reusing code
async def process_image(ctx, choices, player, death=False):
    options = choices[player.roundID]["options"]
    path = "adventure/" + choices[player.roundID]["image"]
    boxpath = "adventure/box.png"
    locations = [(160, 40), (95, 515)]

    if len(options) == 1:
        options = "Reply with '1' to continue."
    elif len(options) == 2:
        options = "1: " + choices[options[0]]["desc"] + "\n2: " + choices[options[1]]["desc"]
    else:
        options = "1: " + choices[options[0]]["desc"] + "\n2: " + choices[options[1]]["desc"] + "\n3:" + choices[options[2]]["desc"]

    title = choices[player.roundID]["title"]
    desc = choices[player.roundID]["text"]
    text = [title, desc]
    await image.send_image(ctx, text, path, locations, 20, (164, 98, 0), user=True, title=True)
    if death:
        await player.user.send("You have fallen, Game over.")
    else:
        await image.send_image(ctx, [options], boxpath, [(25, 25)], 10, (164, 98, 0), user=True, title=True)
