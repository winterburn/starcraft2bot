"""Mainfile for the starcraft bot"""
from collections import defaultdict
import sc2
from sc2.constants import UnitTypeId


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

        await self.military_buildings()
        await self.train_marines()
        await self.saturate_mining()
        await self.build_supply()

    async def build_supply(self):
        """build supply if there is less than 1 supply left"""
        if self.supply_left <= 1:
            # check that we have no supply depots already building
            if not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                pos = await self.find_placement(UnitTypeId.SUPPLYDEPOT,
                                                self.com_cent.position)
                await self.build(UnitTypeId.SUPPLYDEPOT, pos)

    async def saturate_mining(self):
        """Saturate the mining of minerals"""
        if self.com_cent.surplus_harvesters < 0:
            if self.can_afford(UnitTypeId.SCV) and self.com_cent.is_idle:
                self.com_cent.train(UnitTypeId.SCV)

    async def military_buildings(self):
        """Check if there is missing military building and build it"""
        if not self.get_building_count().get(UnitTypeId.BARRACKS):
            if self.can_afford(UnitTypeId.BARRACKS):
                await self.build(UnitTypeId.BARRACKS, near=self.com_cent)

    def get_building_count(self):
        """Count the buildings to dict"""
        count = defaultdict(int)
        for structure in self.structures:
            count[structure.type_id] += 1
        return count

    def get_military_count(self):
        """Count the military units"""
        count = defaultdict(int)
        unit_list = [UnitTypeId.MARINE]
        for unit in unit_list:
            count[unit] = len(self.units.filter(lambda u: u.type_id == unit))
        return count

    async def train_marines(self):
        """Train marines units"""
        barracks = self.structures.filter(lambda u: u.type_id == UnitTypeId.BARRACKS)

        if barracks:
            marine_count = self.get_military_count().get(UnitTypeId.MARINE)
            if marine_count < 20 and self.can_afford(UnitTypeId.MARINE):
                if barracks[0].is_idle:
                    barracks[0].train(UnitTypeId.MARINE)
