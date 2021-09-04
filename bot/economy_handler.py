"""Economy handler class for the bot. Manages the macro level things."""

from sc2.constants import UnitTypeId
from sc2 import position


class EconomyHandler():
    """Handler for the economy of the bot"""

    def __init__(self, bot):
        self.bot = bot

    async def build_supply(self):
        """build supply if there is less than 1 supply left"""
        if self.bot.supply_left <= 1:
            if not self.bot.can_afford(UnitTypeId.SUPPLYDEPOT):
                return
            # check that we have no supply depots already building
            if not self.bot.already_pending(UnitTypeId.SUPPLYDEPOT):
                pos = await self.bot.find_placement(UnitTypeId.SUPPLYDEPOT,
                                                    self.bot.com_cent.position)
                worker = self.bot.workers.filter(lambda u: u.is_idle or u.is_gathering).first
                worker.build(UnitTypeId.SUPPLYDEPOT, pos)

    async def saturate_mining(self):
        """Saturate the mining of minerals"""
        if self.bot.com_cent.surplus_harvesters < 0:
            if self.bot.can_afford(UnitTypeId.SCV) and self.bot.com_cent.is_idle:
                self.bot.com_cent.train(UnitTypeId.SCV)
        building_count = self.bot.get_building_count()
        if building_count.get(UnitTypeId.COMMANDCENTER, 0) * 2 > building_count.get(UnitTypeId.REFINERY, 0):
            if self.bot.can_afford(UnitTypeId.REFINERY):
                geyser = self.get_geyser_near_cc(self.bot.com_cent)
                if geyser:
                    worker = self.bot.workers.random_or(None)
                    worker.build(UnitTypeId.REFINERY, geyser)
        # assign workers to refineries.
        for ref in self.bot.structures.filter(lambda u: u.type_id is UnitTypeId.REFINERY):
            if ref.assigned_harvesters < ref.ideal_harvesters:
                workers = self.bot.workers.filter(lambda u: u.is_idle or u.is_gathering)
                workers.random_or(None).smart(ref)

    def get_geyser_near_cc(self, cc_pos: position.Point2) -> int:
        """Calculates if there is free vespene geyser near given position"""
        for unit in self.bot.vespene_geyser:
            if unit.distance_to(cc_pos) < 20:
                return unit
        return None
