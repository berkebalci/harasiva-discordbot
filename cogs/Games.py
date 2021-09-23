from discord.ext import commands

from random import randint

class games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def dicee(self):
        return randint(1, 6)

    @commands.command(aliases = ["zaratma"]) # Kullanıcının bu komutu kullanmak için illa bu isimi kullanmasına gerek yok.Böylelikle yeni isimler ata-
# yabiliriz.
    async def dice(self,ctx):
        await ctx.send(self.dicee())


def setup(bot):
    bot.add_cog(games(bot))