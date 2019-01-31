import sc2
import sc2.constants as constants
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer


class WinterBot(sc2.BotAI):
    """
    Bot for SC2 made by Winterburn
    """
    cc = None

    async def on_step(self, iteration):
        cc = self.units(constants.UnitTypeId.COMMANDCENTER)
        self.cc = cc.first
        for worker in self.workers:
            if worker.is_idle:
                await self.do(worker.gather(self.state.mineral_field.closest_to(self.cc)))
        await self.saturate_mining(self.cc)
        await self.build_supply()

    async def build_supply(self):
        if self.supply_left <= 1 and not self.units.filter(
                lambda u: u.type_id == constants.UnitTypeId.SUPPLYDEPOT and
                not u.is_ready):
            pos = await self.find_placement(constants.UnitTypeId.SUPPLYDEPOT,
                                            self.cc.position)
            await self.build(constants.UnitTypeId.SUPPLYDEPOT, pos)

    async def saturate_mining(self, cc):
        if cc.surplus_harvesters < 0:
            if self.can_afford(constants.UnitTypeId.SCV) and cc.noqueue:
                await self.do(cc.train(constants.UnitTypeId.SCV))
        
run_game(maps.get("(2)AcidPlantLE"), [
    Bot(Race.Terran, WinterBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)