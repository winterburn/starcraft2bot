"""Run the bot"""
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from bot.bot_main import WinterBot

run_game(maps.get("AcropolisLE"), [
    Bot(Race.Terran, WinterBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
