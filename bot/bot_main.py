"""Mainfile for the starcraft bot"""
import sc2
from sc2 import constants


class WinterBot(sc2.BotAI):
    """
    Bot for SC2 made by Winterburn
    """
    com_cent = None

    async def on_step(self, iteration):
        """Perform one gamestep"""
        self.com_cent = self.townhalls.ready.first
        for worker in self.workers:
            if worker.is_idle:
                worker.gather(self.mineral_field.closest_to(self.com_cent))
        await self.saturate_mining()
        await self.build_supply()

    async def build_supply(self):
        """build supply if there is less than 1 supply left"""
        if self.supply_left <= 1 and not self.units.filter(
                lambda u: u.type_id == constants.UnitTypeId.SUPPLYDEPOT and
                not u.is_ready):
            pos = await self.find_placement(constants.UnitTypeId.SUPPLYDEPOT,
                                            self.com_cent.position)
            await self.build(constants.UnitTypeId.SUPPLYDEPOT, pos)

    async def saturate_mining(self):
        """Saturate the mining of minerals"""
        if self.com_cent.surplus_harvesters < 0:
            if self.can_afford(constants.UnitTypeId.SCV) and self.com_cent.is_idle:
                self.com_cent.train(constants.UnitTypeId.SCV)
