import json
import discord


def init(bot, data):
    with open("config.json") as f:
        config = json.load(f)

    @bot.event
    async def on_ready():
        print("Ludus is ready.")
        print("---")
        await bot.change_presence(activity=discord.Game(config["presence"]))
