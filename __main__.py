"""Run the bot"""
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from starcraft2bot.botMain import WinterBot

run_game(maps.get("(2)AcidPlantLE"), [
    Bot(Race.Terran, WinterBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
