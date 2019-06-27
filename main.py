from discord.ext import commands
import importlib
import json
import os
from threading import Thread
from time import sleep

if not os.path.isfile('config.json'):
    print("Could not find config.json. Read about creating it here: https://mninc.github.io/ludus/")
    input("Press enter to quit.")
    exit()
else:
    with open("config.json") as f:
        config = json.load(f)
if not os.path.isfile('data.json'):
    data = {}
else:
    with open("data.json") as f:
        data = json.load(f)


def save_data():
    while True:
        sleep(10)
        with open("data.json", "w") as f:
            json.dump(data, f)


save_thread = Thread(target=save_data)
save_thread.start()

bot = commands.Bot(command_prefix=config["prefix"])

modules = os.listdir()
for module in modules:
    if module.endswith(".py") and module != "main.py":
        importlib.import_module(module[:-3]).init(bot, data)

bot.run(config["token"])
