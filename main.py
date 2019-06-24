from discord.ext import commands
import importlib
import json
import os

with open("config.json") as f:
    config = json.load(f)
with open("data.json") as f:
    data = json.load(f)

bot = commands.Bot(command_prefix='>')

modules = os.listdir()
for module in modules:
    if module.endswith(".py") and module != "main.py":
        importlib.import_module(module[:-3]).init(bot, data)

bot.run(config["token"])
