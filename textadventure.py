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
        self.squad = ""
        self.damage = 1

    async def set_squad(self, squad):
        self.squad = squad

    async def set_name(self, new_name):
        self.name = new_name

    async def die(self):
        self.alive = False

    async def set_scene(self, new_scene):
        self.roundID = new_scene

    async def set_damage(self, new_damage):
        self.damage = new_damage

    async def set_inv(self, new_inv):
        self.inventory = new_inv


def load_file_text(path):
    with open("res/" + path, "r") as file:
        return file.read()


def init(bot, data):
    introLoad = load_file_text("intro.txt")

    with open("res/choices.json") as f:
        choices = json.load(f)

    @bot.command()
    async def adventure(ctx):
        await begin(ctx)

    # function run on /textadv begin
    async def begin(ctx):
        user = ctx.message.author
        introText = ["Hello traveller, or should I say " + user.name + ".", introLoad]
        await image.send_image(ctx, introText, "black.jpg", [(10, 10), (10, 50)], 25, (255, 255, 255), True)
        player = Player(user.name, user)
        await hypesquad(ctx, player)

    async def hypesquad(ctx, player):
        await player.user.send("--A load of hypesquad lore etc--")
        await player.user.send("Choose your HypeSquad")
        # send hypesquad image
        for i in range(3):
            answer = await reply.get_reply(ctx, 60, player.user)
            if answer:
                answer = answer.content.lower()
                if answer == "bravery" or answer == "brilliance" or answer == "balance":
                    await player.user.send("You chose " + answer)
                    # replace with image
                    await player.set_squad(answer)
                    await story(ctx, player, choices)
                    break
                else:
                    await player.user.send("You didn't enter a house.")
            else:
                await player.user.send("You didn't enter a house.")


async def story(ctx, player, choices):
    alive = player.alive
    while alive:
        # 3 chances to choose
        for i in range(3):
            # e.g ["6", "7", "8"]
            options = choices[player.roundID][player.squad]

            if "death" in options:
                imageText = [choices[player.roundID]["title"], choices[player.roundID]["text"], "Game Over"]
                await image.centre_image(ctx, imageText, "black.jpg", 25, (255, 255, 255), 10, True, player.user)
                alive = False
                break
            elif len(options) == 1:
                imageText = [choices[player.roundID]["title"], choices[player.roundID]["text"]] + ["1: " + choices[options[0]]["desc"]]
                await image.centre_image(ctx, imageText, "black.jpg", 25, (255, 255, 255), 10, True, player.user)
            else:
                imageText = [choices[player.roundID]["title"], choices[player.roundID]["text"]] + [
                    "1: " + choices[options[0]]["desc"], "2: " + choices[options[1]]["desc"], "3: " +
                    choices[options[2]]["desc"]]
                await image.centre_image(ctx, imageText, "black.jpg", 25, (255, 255, 255), 10, True, player.user)

            choice = await reply.get_reply(ctx, 60, player.user)
            if choice:
                choice = choice.content
                if len(options) == 1 and choice == "1":
                    await player.set_scene(options[0])
                    break
                elif choice == "1" or choice == "2" or choice == "3":
                    choice = int(choice)
                    await player.set_scene(options[choice - 1])
                elif choice == "inventory":
                    await display_inventory(ctx, player)
                    break
            else:
                await player.user.send("timeout image here")


async def display_inventory(ctx, player):
    if player.inventory:
        imageText = ["Inventory:", "These are the items you have gathered."] + player.inventory
    else:
        imageText = ["Inventory:", "You haven't found any items."]
    await image.centre_image(ctx, imageText, "black.jpg", 30, (255, 255, 255), 10, True, player.user)
