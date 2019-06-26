from random import randint
import operator
from util.image import centre_image


async def won(user, data):
    if "score" not in data:
        data["score"] = {}
    uid = user.id
    if uid not in data["score"]:
        data["score"][uid] = 0
    score = randint(5, 10)
    data["score"][uid] += score
    return score


async def get_highest(ctx, data):
    highest = list(reversed(sorted(data["score"].items(), key=operator.itemgetter(1))))[:10]
    text = ["Highest scores:"]
    for user, score in highest:
        u = ctx.bot.get_user(int(user))
        text.append(u.display_name + ": " + str(score) + " points")
    await centre_image(ctx, text, "scroll_large.png", 30, (0, 0, 0,))
