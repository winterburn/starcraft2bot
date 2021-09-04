"""Economy handler class for the bot. Manages the macro level things."""

from sc2.constants import UnitTypeId


class EconomyHandler():
    """Handler for the economy of the bot"""

    def __init__(self, bot):
        self.bot = bot

    async def build_supply(self):
        """build supply if there is less than 1 supply left"""
        if self.bot.supply_left <= 1:
            # check that we have no supply depots already building
            if not self.bot.already_pending(UnitTypeId.SUPPLYDEPOT):
                pos = await self.bot.find_placement(UnitTypeId.SUPPLYDEPOT,
                                                    self.bot.com_cent.position)
                await self.bot.build(UnitTypeId.SUPPLYDEPOT, pos)

    async def saturate_mining(self):
        """Saturate the mining of minerals"""
        if self.bot.com_cent.surplus_harvesters < 0:
            if self.bot.can_afford(UnitTypeId.SCV) and self.bot.com_cent.is_idle:
                self.bot.com_cent.train(UnitTypeId.SCV)
