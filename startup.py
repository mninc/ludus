import json
import discord
import asyncio


async def cycle_games(bot):
    games = ["Battleships", "Chess", "Connect 4", "Hangman", "Rock, Paper, Scissors", "Tic Tac Toe", "Trivia",
             "Would You Rather"]
    while True:
        for game in games:
            await bot.change_presence(activity=discord.Game(game))
            await asyncio.sleep(12)


def init(bot, data):
    with open("config.json") as f:
        config = json.load(f)

    @bot.event
    async def on_ready():
        print("Ludus is ready.")
        print("---")
        await cycle_games(bot)

