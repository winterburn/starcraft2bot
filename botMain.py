import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

class WinterBot(sc2.BotAI):
    """
    Bot for SC2 made by Winterburn
    """
    async def on_step(self, iteration):
        if iteration == 0:
            for worker in self.workers:
                await self.do(worker.attack(self.enemy_start_locations[0]))

run_game(maps.get("(2)AcidPlantLE"), [
    Bot(Race.Zerg, WinterBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)