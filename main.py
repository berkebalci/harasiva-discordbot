import discord
from discord.ext import commands,tasks
import os
from cogs import commandss

# Aşağıdaki kodta amacımız serverdaki küfüleri engellemek

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True, guild_messages=True)
# Intentsler botumuzla tam olarak ne yapmak istedğimizi belirten değişkenlerdir.
# Bu modülde Intents adlı bir sınıf var ve böylece amacımızı belirtebiliyoruz.
# Ve bunu da Bot(İlla Bot isimli sınıf olması gerekmez.Bot isimli sınıfın ebeveyni olan Client isimli sınıfı da yazabiliriz.)
# isimli sınıfın argümanında belirtmemiz gerek.(Aşağıdaki kodta.)


client = commands.Bot(command_prefix= "!dc ",intents= intents)



# Bir Not:Yukarıda Bot isimli sınıfı kullandık.Aslında aşağıdaki işlemleri Client isimli ana sınıfın  yardımı ile yaptık.
# Yani bu 'Bot' isimli sınıf 'Client' isimli ana sınıfn alt sınıfıdır.



with open("Badwords.txt", "r", encoding="utf-8") as f:
    word = f.read()
    badwords = word.split(",")

swearword_count = dict()
hata_ayiklama = dict()                            #Bu sözlüğü birlikte kullanıcıların banlanma durumlarında kullanacağiz.
Oto_mute = 1                       #Botun mutelemesini açmak isteyenler için kolaylık.
mod_names = []
class Social:
    TWITTER = "https://twitter.com/"
    INSTAGRAM = "https://instagram.com/"
    YOUTUBE = "https://youtube.com/"
    LINKEDIN = "https://www.linkedin.com/in/"

all_social_medias = {
    "TWITTER":"HaraSivaaa",
    "INSTAGRAM":"harasivaaa",
    "YOUTUBE":"BerkeBalcı",
    "LINKEDIN":"berke-balcı-1b591321b/"}


Room = 0
@client.command(aliases= ["sosyal_medya"])
async def setSocialmed(ctx, s ,abolute_path):  #Sosyal medya linklerini değiştirmemizi sağlar.
    # s değeri hangi socila media hesabını değiştirmek istediğini belirtecek.
    # abolute_path ifadesi sosyal medya linki
    """Must be YOUTUBE,INSTAGRAM,TWITTER or LINKEDIN links   """
    all_social_medias[s] = abolute_path
    print(all_social_medias)

@client.command()
async def socialpush(ctx, room:discord.TextChannel):  #Bu sosyal medya linki gönderme olayını başlatan bu fonksiyon.
    global Room
    Room = room
    await socialmedia_push.start()

@client.command()
async def stop_socialpush(ctx):
    socialpush.stop()

@tasks.loop(minutes= 0.06,count=3)
async def socialmedia_push():
    await Room.send(getSocials())


def getSocials() -> str:
    return f"""
    {Social.TWITTER}{all_social_medias.get("TWITTER")}
    {Social.YOUTUBE}{all_social_medias.get("YOUTUBE")}
    {Social.INSTAGRAM}{all_social_medias.get("INSTAGRAM")}
    {Social.LINKEDIN}{all_social_medias.get("LINKEDIN")}
"""

@client.event  # Bu decoratorları botumuza özellik eklemek için kullanıcaz.
async def on_ready():  # Bu arada buradaki fonksiyonların isimleri önemli çünkü modülde bu fonksiyon isimleri ile decoratorlar
    # **birbirine bağlanıyorlar.

    print("I am ready!")
    print("MEMBERS:")


    for members in client.get_all_members():
        print(members)

                                # Buradaki client ifadesi 12.satırdaki Bot isimli sınıfın bir objesidir.



                                        # client.get_all_members() ifadesi bir generator'dur
    await client.change_presence(activity=discord.Game(name="with the code"))

    #Yukarıdaki kod discord botunun durumunda Kodlama oynuyor yazdıaracak 3 adet daha durum var bunlar:

    #Streaming:await client.change_presence(activity=discord.Streaming(name="Kodlama",url = 'twitch adresinin url'si'))
    #Listening:await client.change_presence(activity=discord.Activity(type= discord.ActivityType.listening, name= 'Bir şarkı ismi'))
    #Watching:#Listening:await client.change_presence(activity=discord.Activity(type= discord.ActivityType.watching, name= 'Bir film ismi'))






@client.command()
async def stop_otomute(ctx):
    global Oto_mute
    Oto_mute = 0
    print("Oto_mute has eveluated to 0")

@client.event
async def on_message(message):   #message.author.id ifadesinin türü int'dir. message.content 'str' döndürür.

    global mod_names
    global swearword_count
    global badwords
    global Oto_mute




      # Buradaki client ifadesi 12.satırdaki Bot isimli sınıfın bir objesidir.



    # Ayrıca message.author.name kullanıcının string türünden ismini veriyor.


    if message.author == client.user:  # Burada eğer mesaj bot tarafından yazılıp yazılmadığını kontrol ediyor.
        await client.process_commands(message)


    else:
        if Oto_mute != 1:
            await client.process_commands(message)
        else:
            msg = message.content
            #guild = message.channel
            #member = discord.Member


            for x in badwords:


                try:
                    if x in msg:


                        if hata_ayiklama[str(message.author.id)] == 0:
                            swearword_count[str(message.author.id)] += 1
                        if swearword_count[str(message.author.id)] > 5 and hata_ayiklama[str(message.author.id)] == 0:
                            await message.author.send("Sunucudan Çok fazla küfür ettiğiniz için susturuldunuz.")
                        await message.channel.send("Lütfen bu kötü ifadeyi kullanmayınız.")
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
async def on_member_join(member):  # type(member.name) dediğimizde sonuç string çıkıyor.
    channel = discord.utils.get(member.guild.text_channels, name="hosgeldiniz")
    await channel.send(f"{member.name} isimli kullanıcı aramıza katıldı.")
    global swearword_count
    swearword_count[str(member.id)] = 0
    hata_ayiklama[str(member.id)] = 0
    dm_channell = await member.create_dm()
    await dm_channell.send(f"{member},aramıza hoşgeldin:)")

@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="aramizdan-ayrilanlar")
    await channel.send(f"{member.name},elveda:(")
# Burada print(member) dediğimizde çıkan sonuç isim#.... ifadesi.
# type(member) ifadesinde ise sonuç class 'discord.member.Member' oluyor.

@client.command()
async def send_timed_msg(ctx,*args):
    text = ""
    for x in args:
        text = text + " " + x
    await send_timed_messages.start(text)


    # Twitter = https://twitter.com/HaraSivaaa
    # Instagram = https://www.instagram.com/harasivaaa/?hl=tr
    # Youtube = https://www.youtube.com/channel/UCBlwzOXsdt8U8hIgIia-E-w
#####################Çalışmayan Komut#######################
@client.command()
async def change_interval(*, minutes= 0):

    send_timed_messages.change_interval(minutes= minutes)
#######################Çalışmayan Komut######################

@tasks.loop(minutes= 0.06,count= 2)  # Bu ifade ile birlikte aşağıdaki methodumuz loop'a giriyor ve belirttiğimiz aralıklarla tekrar çalışıyor.
async def send_timed_messages(msg,time=0,count=0):  # count ifadesine verdiğimiz sayı kadar fonksiyon çalıştığında,fonksiyon çalışmayı durdurur
    for x in client.get_all_channels():
        if x.id == 886984276342620170:
            await x.send(msg)





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


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")



client.run('ODcyODgyMTAwNTQ4ODIxMDIy.YQwUzg.v0KB8RdiecfMOFK65SiP2C25knc')

# Buradaki parantez içerisine 'Token' isimli argüman gelir.Tokenlar script(kod dizisi) dosyaları ile bot-
# **umuzu birbirine entegre eden keylerdir.
# Token değeri her bot için farklıdır.

# async :  async nın anlamı asenktron demektir.O da kendi kendine,bağımsız çalışan demektir.Buradan da gördüğümüz
# **gibi fonksiyonlar birbirinden bağımsız çalışıyor.Ve herhangi bir çağırılma durumları olmuyorlar.
