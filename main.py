# 1 # bilgi satırı ya da yorum
# 4 # oranın geliştirilebileceğini gösterir.
import discord
from discord.ext import commands
import os
from cogs import *
import Utlissss
import asyncio

# Aşağıdaki kodta amacımız serverdaki küfüleri engellemek

intents = discord.Intents.all()

# Intentsler botumuzla tam olarak ne yapmak istedğimizi belirten değişkenlerdir.
# Bu modülde Intents adlı bir sınıf var ve böylece amacımızı belirtebiliyoruz.
# Ve bunu da Bot(İlla Bot isimli sınıf olması gerekmez.Bot isimli sınıfın ebeveyni olan Client isimli sınıfı da yazabiliriz.)
# isimli sınıfın argümanında belirtmemiz gerek.(Aşağıdaki kodta.)


client = commands.Bot(command_prefix= "!dc ",intents= intents)


# Bir Not:Yukarıda Bot isimli sınıfı kullandık.Aslında aşağıdaki işlemleri Client isimli ana sınıfın  yardımı ile yaptık.
# Yani bu 'Bot' isimli sınıf 'Client' isimli ana sınıfn alt sınıfıdır.


for bad in Utlissss.bad_words:
    for bad_2 in bad:
        badwords = bad_2.split(",")

swearword_count = dict()
hata_ayiklama = dict()                            #Bu sözlüğü birlikte kullanıcıların banlanma durumlarında kullanacağiz.
Oto_mute = 1                       #Botun mutelemesini açmak isteyenler için kolaylık.
num_swearwords = 3
other_roles = []
mod_roles = [889933119875055716]
owner_roles = [879006772629749841]


reaction_number1 = 0
ext_file_types = ["jpeg","jpg","png","gif"]


@client.event  # Bu decoratorları botumuza özellik eklemek için kullanıcaz.
async def on_ready():  # Bu arada buradaki fonksiyonların isimleri önemli çünkü modülde bu fonksiyon isimleri ile decoratorlar
    # **birbirine bağlanıyorlar.

    print("I am ready!")




    # client.get_all_members() ifadesi bir generator'du
#members.bot ifadesi bir boolean değer döndürüp member bot ise True değilse False döndürüyor
#members.guild.roles sunucudaki insanların role id'sini ve rollerini döndürüyor.
    await client.change_presence(activity=discord.Game(name="with the code"))



    #Yukarıdaki kod discord botunun durumunda Kodlama oynuyor yazdıaracak 3 adet daha durum var bunlar:

    #Streaming:await client.change_presence(activity=discord.Streaming(name="Kodlama",url = 'twitch adresinin url'si'))
    #Listening:await client.change_presence(activity=discord.Activity(type= discord.ActivityType.listening, name= 'Bir şarkı ismi'))
    #Watching:#Listening:await client.change_presence(activity=discord.Activity(type= discord.ActivityType.watching, name= 'Bir film ismi'))

@client.event
async def on_message(message):
    if len(message.attachments) > 0 and message.channel.name.startswith("questions"):
        for ext in ext_file_types:
            if message.attachments[0].filename.endswith(ext):
                await message.add_reaction("🅰")
                await message.add_reaction("🅱")
                await message.add_reaction("🇨")
                await message.add_reaction("🇩")
                await message.add_reaction("🇪")
                reaction_number1 = 5
                break
            ####Buraya ekstra şeyler eklenebilir
    # Bu modülde discord server'ına yüklenmiş mesajlar otomatikman tutturulur.# #Yükleme olmayan mesajlarda mesajlar tutturulmaz.
    # Yukarıdaki ifadenin çıktısı:
    # [<Attachment id=890718624325722132 filename='pp.jfif' url='https://cdn.discordapp.com/attachments/873962539975839784/890718624325722132/pp.jfif'>]
    global swearword_count
    global hata_ayiklama
    global num_swearwords

    if message.author == client.user:  # Burada eğer mesaj bot tarafından yazılıp yazılmadığını kontrol ediyor.
        await client.process_commands(message)
    else:
        if Oto_mute != 1:
            await client.process_commands(message)
        else:
            msg = message.content

            for x in badwords:
                try:
                    if x in msg:
                        if hata_ayiklama[str(message.author.id)] == 0:
                            swearword_count[str(message.author.id)] += 1
                        if swearword_count[str(message.author.id)] > num_swearwords and hata_ayiklama[
                            str(message.author.id)] == 0:
                            mod_role = discord.utils.get(message.guild.roles, name="Mod")
                            mod = mod_role.members
                            #awit x.send(f"{message.author},has wrotten a lot of badwords into the chatbox.")
                            await mute_person(message, message.author, "1h", "For too many bad words.")
                        # TypeError: mute() takes from 3 to 4 positional arguments but 5 were given
                        # could not convert string to float: 'For too many badwords'
                        await message.channel.send("Lütfen bu kötü ifadeyi kullanmayınız.Yoksa banlanacksınınz")
                        await message.delete()


                except KeyError:
                    hata_ayiklama[str(message.author.id)] = 0
                    swearword_count[str(message.author.id)] = 1
                    await message.author.send("Bu ifadeyi kullanmaya devam edersiniz mutelanıcaksınız.")
                    await message.channel.send("Lütfen bu kötü ifadeyi kullanmayınız.")
                    await message.delete()
                    break
            await client.process_commands(message)
            # Bu fonksiyon on_message event'inde default olarak bulunmalıdır.Eğer on_message
            # eventini kullanacaksak ve komutarımızın programın geri kalanında düzgün çalışmasını
            # istiyorsak bu fonksiyonu kullanmalıyız # burada iki adet parametre kullanamayız çünkü on_message event'i tek argüman al


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if  (payload.channel_id == 890734899135393814): #Buradaki id questions 2 adlı channelin id'sidir
        channell = await client.fetch_channel(payload.channel_id)
        messagee = await channell.fetch_message(payload.message_id)  #messagee'in türü Message isimli sınıfa obje.
        for reaction in messagee.reactions:     # checks the reactant isn't a bot and the emoji isn't the one they just reacted with

            if reaction_number1 >= 5  and not payload.member.bot and str(reaction) != str(payload.emoji):
                # removes the reaction
                await messagee.remove_reaction(reaction.emoji, payload.member)

@client.event
async def on_command_error(ctx,error):
    await ctx.send(error)
@client.event
async def on_member_update(before, after):
    global mod_roles
    global other_roles
    if len(before.roles) < len(after.roles):
        # The user has gained a new role, so lets find out which one
        newRole = next(role for role in after.roles if role not in before.roles)
        if newRole.name == "Muted":
            await after.send("Your role has just become 'Muted'")

        elif newRole.id == 889933119875055716:
            await after.send("Congratulations!Your role has been upgraded to 'Mod'")
        if not newRole.id in mod_roles:
            if not newRole.name in after.guild.roles:
                other_roles.append(newRole.id)
                if  not (newRole.name == "Muted"):
                    await after.send(f"Congratulations!Your role has been upgraded to {newRole.name}")
            # This uses the name but you could always use newRole.id == Roleid here
            # Now, simply put the code you want to run whenever someone gets the "Respected" role here

#commands.check() decorator'u aldığı fonksiyonun True mu False mu döndürdüğüne bakar.True döndürürse,onun altındaki method
#**çalışır.False ise çalışmaz.

@client.event
async def on_member_join(member):  # type(member.name) dediğimizde sonuç string çıkıyor.
    channel = discord.utils.get(member.guild.text_channels, name="hosgeldiniz")
    await channel.send(f"{member.name} isimli kullanıcı aramıza katıldı.")
    global swearword_count
    swearword_count[str(member.id)] = 0
    hata_ayiklama[str(member.id)] = 0
    dm_channell = await member.create_dm()
    await dm_channell.send(f"{member},aramıza hoşgeldin:)")


@client.event #Bu ifade bu modlüdeki eventlerle aynı görevde işlem yapmaktadır.
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="aramizdan-ayrilanlar")
    await channel.send(f"{member.name},elveda:(")


# Burada print(member) dediğimizde çıkan sonuç isim#.... ifadesi.
# type(member) ifadesinde ise sonuç class 'discord.member.Member' oluyor.


def to_upper(argument):  #Converterlarda böyle bi yapı da vardır.Convertarlara çağırılabilen her şeyi koyabiliriz.Örnek:
                         #content: to_upper isimli convertırda ki to_upper kısmı.Bu kısım bir fonksiyon ve fonksiyonlar
                         #çağırılabilir şeylerdir.
    return argument.upper()

@client.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)

async def mute_person(ctx, member: discord.Member, time=None,reason = None):
    #ctx = message

    if not member:
        await ctx.channel.send("You must mention a member to mute!")
    elif not time:
        await ctx.channel.send("You must mention a time!")
    else:
        if not reason:
            reason = "No reason given"
        # Now timed mute manipulation
        try:
            seconds = float(time[:-1])  # Gets the numbers from the time argument, start to -1
            duration = time[-1]  # Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await ctx.channel.send("Invalid duration input")
                return

        except Exception as e:
            print(e)
            await ctx.channel.send("Invalid time input")
            return
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                              read_message_history=True,
                                              read_messages=False)
        await member.add_roles(mutedRole, reason=reason)
        muted_embed = discord.Embed(title="Muted user",
                                    description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}",
                                    colour=discord.Colour.purple())
        await ctx.channel.send(embed=muted_embed)
        await asyncio.sleep(seconds)
        await member.remove_roles(mutedRole)
        unmute_embed = discord.Embed(title="Mute over!",
                                     description=f'{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}')
        await ctx.channel.send(embed=unmute_embed)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")  #Burada cogs...... değer girerken ifadenin sonunda .py olmamalı.
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
#Eğer botun her çalıştığında bu python dosyalarımızın botumuza yüklenmesini istiyorsak şunu yapmalıyız.
#os modlünü aktif hale getirmeliyiz.Çünkü listdir() isimli moethod bize bu klasorde bulunan dosya isimlerini verir.

#Bu fonksiyonuda yüklemek istediğimiz python dosyalarında değişiklik yaptığımızda bu değişiklikleri pythonun tekrar okuması için kullandık.
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")








client.run('ODcyODgyMTAwNTQ4ODIxMDIy.YQwUzg.v0KB8RdiecfMOFK65SiP2C25knc')

# Buradaki parantez içerisine 'Token' isimli argüman gelir.Tokenlar script(kod dizisi) dosyaları ile bot-
# **umuzu birbirine entegre eden keylerdir.
# Token değeri her bot için farklıdır.

# async :  async nın anlamı asenktron demektir.O da kendi kendine,bağımsız çalışan demektir.Buradan da gördüğümüz
# **gibi fonksiyonlar birbirinden bağımsız çalışıyor.Ve herhangi bir çağırılma durumları olmuyorlar.
