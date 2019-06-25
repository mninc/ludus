# .____              .___
# |    |    __ __  __| _/_ __  ______
# |    |   |  |  \/ __ |  |  \/  ___/
# |    |___|  |  / /_/ |  |  /\___ \
# |_______ \____/\____ |____//____  >
#         \/          \/          \/


class Player:
    alive = True
    choice = 0

    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.squad = ""

    async def set_squad(self, squad):
        self.squad = squad

    async def set_name(self, new_name):
        self.name = new_name

    async def die(self):
        self.alive = False

    async def set_choice(self, new_choice):
        self.choice = new_choice


def init(bot, data):
    @bot.command()
    async def textadv(ctx, *args):
        if args[0] == "begin":
            await begin(ctx)
        else:
            pass


# function run on /textadv begin
async def begin(ctx):
    user = ctx.message.author
    await user.send("begin game")
    player = Player(user.name, user)


async def ask_squad(ctx, player):
    await player.user.send("--A load of hypesquad lore etc--")
    await player.user.send("Choose your HypeSquad")
