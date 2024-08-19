from .markov import MarkovCog

async def setup(bot):
    await bot.add_cog(MarkovCog(bot))