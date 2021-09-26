import discord
from discord.ext import commands
import random


class Commands(commands.Cog):
    def __init__(self, bot):    #Buradaki 'bot' ifesi data field olarak adlandırılıyormuş.
        self.bot = bot
        self.activities = {}

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hellooo")

    @commands.command()
    async def giveaway(self, ctx):
        while True:
            a = random.choice(self.bot.guilds[0].members)         #Bu arada bot.guilds ifadesi de bir liste döndürüyor
            if a.id == 872882100548821022:
                continue
            else:
                await ctx.send(f"{a},won the giveway,congratulations :)")

    @commands.command()
    async def change_status(self,ctx, activity, *, text):
        self.bind_text(text)
        await self.bot.change_presence(**self.activities.get(activity))  #Böyle yaparak dict objesini unpack ettik.

    @commands.command()
    async def change_status(self, ctx, activity, url,*, text):
#Görüldüğü gibi yukarıdaki iki methodta neredeyse aynıdır.Python burada parametrelere bakıyor,hangisinde argüman sayısı fazlaysa onu çalıştırıyor.
        self.bind_text(text, url)
        await self.bot.change_presence(**self.activities.get(activity))  # Böyle yaparak dict objesini unpack ettik.


    def bind_text(self, text, url= ""):
        self.activities = {
          "1":{"activity": discord.Game(name=text)},
          "2":{"activity": discord.Activity(type=discord.ActivityType.listening, name=text)},
          "3":{"activity": discord.Activity(type=discord.ActivityType.watching, name=text)},
          "4":{"activity": discord.Streaming(name= text,url= url)},
        }






    @commands.command(aliases=["selamla"])
    async def greetings(self,ctx, *args):  # ctx demek context yani mesajın içeriği anlamına geliyor
        print(ctx)  # Bunu yazdırdığımızda <Message id=878026076855623711 channel=<TextChannel id=873962539......
        print(
            ctx.message.channel)  # gibi devam eden bir text beliriyor.Discord bu text içinden mesajın bulunduğu kanalı alıp aşağıdaki
        # kodu çalıştırıyor.
        # Ayrıca bu yapıdan da discord'un bir kişi o channel'a yazı yazdığında o kişinin birçok bilgisine ulaşmamıza yardımcı
        # olduğunu da anlamamız gerekir.
        await ctx.send("Selamlar herkese ben discord botu.")

    @commands.command(aliases=["mesajlari_temizle"])
    @commands.has_role("admin")  # Bu kodla bu temizleme işlemini sadece admin rolüne sahip kullanıcı yababilecek
    async def clear(self,ctx, amount):  # Bu method ile birlikte de bir kanaldaki mesajları silebileceğiz.
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f"{amount} kadar mesaj bu kanaldan silinmiştir.")
    @clear.error
    async def clear_error(self,ctx,error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Lütfen komutta gerekli boşlukları doldurun.")


    @commands.command(aliases=["sunucuyu_kopyala"])
    async def copy_channel(self,ctx, amount=1):
        for x in range(amount):
            await ctx.channel.clone()


    @commands.command(aliases=["kick"])
    @commands.has_role("admin")
    async def kick_user(self,ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member} adlı kullanıcı sunucudan kicklenmiştir.")


    @commands.command(aliases=["ban"])
    @commands.has_role("admin")
    async def ban_user(self,ctx, member: discord.Member, *, reason=None):
        dm_channel = await member.create_dm()
        await dm_channel.send("You've been banned from the server.You won't join the server until admin opens your ban.")
        await member.ban(reason=reason)
        await ctx.send(f"{member} isimli kullanıcı sunucudan banlanmıştır.")








    @commands.command()
    async def banned_list(self,ctx):
        banned_users = await ctx.guild.bans()
        if banned_users == []:
            print("Bu serverda hiç banlanan kullanıcı yoktur.")
        else:
            for bans in banned_users:
                kullanici1 = bans.user
                print(kullanici1.name, kullanici1.discriminator)

        # for x in banned_users diyip x'i yazırdığımızda şu sonuç çıkıyor(servarda banlı 1 kişi var.)
        # BanEntry(reason='Adam 31sjsj dedi abi', user=<User id=805458746394148935 name='Harasivaaa' discriminator='8603' bot=False>)



    @commands.command(aliases=["unban"])
    @commands.has_role("admin")
    async def unban_user(self,ctx, *, member):
        # Burada *(asterisk) kullanmamızın sebebi *'dan sonraki her argümanın member objesine
        # gitmesini istememizdir.Çünkü eğer böyle yapmasak ve birinin banını kaldırmak istesek:
        # !dc unban Harasiva Balcı böylece Harasiva ve Balcı ayrı birer parametreler olarak
        # görülecek ve adamın banını açamayacağız.

        banned_users = await ctx.guild.bans()  # Bu ifade banlanmış kulanıcıların bir listesini döndürecek.
        member_name, member_discriminator = member.split(
            "#")  # Kullancıyı unban için kullanıcının adının yanında yazan discriminatora da'ihtiyaç var.
        # Harasiva#5689 mesela.
        print(banned_users)
        print(member_name)
        print(member_discriminator)
        for bans in banned_users:
            kullanici = bans.user

            if (kullanici.name, kullanici.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(kullanici)
                await ctx.send(f"{kullanici.name} isimli kullanıcının banı kaldırılmıştır.")
                return
            else:
                print("Bir hata oluştu.")

    # Aşağıdaki kodlar coglar ve sınıflama ile alakalıdır.Amacımız bir python dosyası yüklemek.
    @commands.command(description="Mutes the specified user.")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("admin")
############################              AlıntıKod         ###############################################
    async def mute(self,ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)
        embed = discord.Embed(title="muted", description=f"{member.mention} was muted ",
                              colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("admin")
    async def unmute(self,ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f" you have unmutedd from: - {ctx.guild.name}")
        embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",
                              colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)


    @commands.command(description= "Adds reaction to the message that you've sent ")
    @commands.has_permissions(manage_messages= True)
    @commands.has_role("admin")
    async def add_reaction(ctx,emoji = 0):
        pass

################################      AlıntıKod        ####################
def setup(bot):
    bot.add_cog(Commands(bot))  #Burada setup isimini kullanmak önemli çünkü bot bu isme bakarak bu sınıfın bir cog olduğunu anlıyor ve
                                #ona göre işlem yapıyor.
