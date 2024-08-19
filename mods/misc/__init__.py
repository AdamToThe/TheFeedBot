from .misc import MiscCog

async def setup(bot):
    await bot.add_cog(MiscCog(bot))
