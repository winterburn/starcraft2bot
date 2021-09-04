"""Mainfile for the starcraft bot"""
from collections import defaultdict
import sc2
from sc2.constants import UnitTypeId
from bot.economy_handler import EconomyHandler


class WinterBot(sc2.BotAI):
    """
    Bot for SC2 made by Winterburn
    """
    com_cent = None

    def __init__(self, *args, **kwargs):
        self.eco = EconomyHandler(self)
        super().__init__(*args, **kwargs)

    async def on_step(self, iteration):
        """Perform one gamestep"""
        self.com_cent = self.townhalls.ready.first
        for worker in self.workers:
            if worker.is_idle:
                worker.gather(self.mineral_field.closest_to(self.com_cent))

        await self.military_buildings()
        await self.train_marines()
        await self.eco.saturate_mining()
        await self.eco.build_supply()

    async def military_buildings(self):
        """Check if there is missing military building and build it"""
        barracks_count = self.get_building_count().get(UnitTypeId.BARRACKS, 0)
        if barracks_count < 4:
            if self.can_afford(UnitTypeId.BARRACKS):
                # special placement for first barracks
                if barracks_count == 0:
                    worker = self.workers.filter(lambda u: u.is_gathering).first
                    print("barracks now", worker)
                    worker.build(UnitTypeId.BARRACKS,
                                 self.main_base_ramp.barracks_correct_placement)
                else:
                    await self.build(UnitTypeId.BARRACKS, near=self.com_cent,
                                     placement_step=10)

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
            for instance in barracks:
                if self.can_afford(UnitTypeId.MARINE) and instance.is_idle:
                    instance.train(UnitTypeId.MARINE)
