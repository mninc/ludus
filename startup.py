import discord
import asyncio


async def cycle_games(bot):
    # cycle through the games we have as fast as the rate limit allows
    games = ["Battleships", "Chess", "Connect 4", "Hangman", "Rock, Paper, Scissors", "Tic Tac Toe", "Trivia",
             "Would You Rather", "2048"]
    
    while True:
        for game in games:
            await bot.change_presence(activity=discord.Game(game))
            await asyncio.sleep(12)


def init(bot, data):
    @bot.event
    async def on_ready():
        print("Ludus is ready.")
        print("---")
        await cycle_games(bot)
