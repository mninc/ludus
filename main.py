from discord.ext import commands
import importlib
import json
import os
from threading import Thread
from time import sleep

# check if config file exists
if not os.path.isfile('config.json'):
    print("Could not find config.json. Read about creating it here: https://mninc.github.io/ludus/")
    input("Press enter to quit.")
    exit()
else:
    # load config file
    with open("config.json") as f:
        config = json.load(f)

# check if data file exists
if not os.path.isfile('data.json'):
    # make data dictionary, this will be saved later
    data = {}
else:
    # load data file
    with open("data.json") as f:
        data = json.load(f)


def save_data():
    # save data every 10 seconds
    while True:
        sleep(10)
        with open("data.json", "w") as f:
            json.dump(data, f)


# start data saving thread
save_thread = Thread(target=save_data)
save_thread.start()

# initialise bot
bot = commands.Bot(command_prefix=config["prefix"])

# get all python files in current directory and initialise them
modules = os.listdir()
for module in modules:
    if module.endswith(".py") and module != "main.py":
        importlib.import_module(module[:-3]).init(bot, data)

# start the bot
bot.run(config["token"])
