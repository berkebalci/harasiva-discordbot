import discord
from discord.ext import commands,tasks
import random,main



class Talking_to_bot(commands.Cog):
    def __init__(self, bot):    #Buradaki 'bot' ifesi data field olarak adlandırılıyormuş.
        self.bot = bot
        self.activities = {}

    @commands.command(aliases=["selamla"])
    async def greetings(self,ctx, *args):  # ctx demek context yani mesajın içeriği anlamına geliyor
        print(ctx)  # Bunu yazdırdığımızda <Message id=878026076855623711 channel=<TextChannel id=873962539......
        print(
            ctx.message.channel)  # gibi devam eden bir text beliriyor.Discord bu text içinden mesajın bulunduğu kanalı alıp aşağıdaki
        # kodu çalıştırıyor.
        # Ayrıca bu yapıdan da discord'un bir kişi o channel'a yazı yazdığında o kişinin birçok bilgisine ulaşmamıza yardımcı
        # olduğunu da anlamamız gerekir.
        await ctx.send(f"Hi everyone,my name is {main.client.user.name}.  I am a Discord Bot :) ")
    @commands.command()
    async def chat(self,ctx):
        pass
def setup(bot):
    bot.add_cog(Talking_to_bot(bot))  #Burada setup isimini kullanmak önemli çünkü bot bu isme bakarak bu sınıfın bir cog olduğunu anlıyor ve
                                #ona göre işlem yapıyor.
