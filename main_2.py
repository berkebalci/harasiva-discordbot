import discord
from discord.ext import commands,tasks
import os
import Utlissss
import asyncio
import aiohttp
import random



intents = discord.Intents.all()

client = commands.Bot(command_prefix= "!dc ",intents= intents)

for bad in Utlissss.bad_words:
    for bad_2 in bad:
        badwords = bad_2.split(",")

swearword_count = dict()
hata_ayiklama = dict()
Oto_mute = 1
num_swearwords = 3
other_roles = []
mod_roles = [889933119875055716]
owner_roles = [879006772629749841]

reaction_number1 = 0
ext_file_types = ["jpeg","jpg","png","gif"]

@client.event
async def on_ready():
    print("I am ready!")
    await client.change_presence(activity=discord.Game(name="with the code"))

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

    # Yukarıdaki ifadenin çıktısı:
    # [<Attachment id=890718624325722132 filename='pp.jfif' url='https://cdn.discordapp.com/attachments/873962539975839784/890718624325722132/pp.jfif'>]
    global swearword_count
    global hata_ayiklama
    global num_swearwords

    if message.author == client.user:
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



@client.event
async def on_member_join(member):
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





def to_upper(argument):  #Converterlarda böyle bi yapı da vardır.Convertarlara çağırılabilen her şeyi koyabiliriz.Örnek:
                         #content: to_upper isimli convertırda ki to_upper kısmı.Bu kısım bir fonksiyon ve fonksiyonlar
                         #çağırılabilir şeylerdir.
    return argument.upper()


@client.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)
#################  Help    #########################
@client.command()
async def commands(): #Bu Botta olan özellikleri gösteren komut olacak
    pass
################   BOT   ##############

@client.command(description= "For that command there are a few options"
                            "Playing xxx >>> !dc change_status 1 game_name"
                            "Listening xxx >>> !dc change_status 2 music_name"
                            "Watching xxx >>> !dc change_status 3 video_name")
async def change_status(ctx, activity, *, text):

    """Changes bot's status"""
    activities = {
        "1": {"activity": discord.Game(name=text)},
        "2": {"activity": discord.Activity(type=discord.ActivityType.listening, name=text)},
        "3": {"activity": discord.Activity(type=discord.ActivityType.watching, name=text)},
        }
    # Görüldüğü gibi yukarıdaki iki methodta neredeyse aynıdır.Python burada parametrelere bakıyor,hangisinde argüman sayısı fazlaysa onu çalıştırıyor.

    await client.change_presence(**activities.get(activity))  # Böyle yaparak dict objesini unpack ettik.

###############   Bot_Response  ##############
@client.command(aliases=["selamla"])
async def greetings(ctx, *args):  # ctx demek context yani mesajın içeriği anlamına geliyor
    print(ctx)  # Bunu yazdırdığımızda <Message id=878026076855623711 channel=<TextChannel id=873962539......
    print(
        ctx.message.channel)  # gibi devam eden bir text beliriyor.Discord bu text içinden mesajın bulunduğu kanalı alıp aşağıdaki
    # kodu çalıştırıyor.
    # Ayrıca bu yapıdan da discord'un bir kişi o channel'a yazı yazdığında o kişinin birçok bilgisine ulaşmamıza yardımcı
    # olduğunu da anlamamız gerekir.
    await ctx.send(f"Hi everyone,my name is {client.user.name}.  I am a Discord Bot :) ")
@client.command()
async def chat(ctx):
    pass

###############  Fun  ##################################

allowed_animal = ["dog", "cat", "panda", "fox", "red panda", "koala", "bird", "raccoon", "kangaroo"]
@client.command()
async def giveaway(ctx):
    while True:
        a = random.choice(ctx.guild.members)  # Bu arada bot.guilds ifadesi de bir liste döndürüyor
        if a.bot:
            continue
        else:
            await ctx.send(f"{a},won the giveway,congratulations :)")
            break

@client.command()
async def animal_fact(ctx,animal : str):
    global allowed_animal
    if not(animal in allowed_animal):
       await ctx.send("You can use that command for these animals:\n"
                      "dog\n"
                      "cat\n"
                      "panda\n"
                      "fox\n"
                      "red panda\n"
                      "koala\n"
                      "bird\n"
                      "raccoon\n"
                      "kangaroo\n")


    elif any([x.isupper() for x in animal]):
        await ctx.send("Please use lower case letters.")
    else:


        async with aiohttp.ClientSession() as session:

            request = await session.get(f'https://some-random-api.ml/img/{animal}')
            dogjson = await request.json() #dogjson objesi bir dict'dir.
            print(type(request))
            # This time we'll get the fact request as well!
            request2 = await session.get(f'https://some-random-api.ml/facts/{animal}')
            factjson = await request2.json()

        embed = discord.Embed(title="FACT!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


@client.command()
async def meme(ctx):
    """Sends random meme to the channel"""
    async with aiohttp.ClientSession() as r:
        request = await r.get("https://some-random-api.ml/meme")  #Bu API mantığına bakmam gerek.
        rjson = await request.json()

    embed = discord.Embed(
        title= "Random Meme",
        colour= discord.Colour.orange())

    print(rjson)
    embed.set_image(url=rjson['image'])


    await ctx.send(embed= embed)

############  Games  ################

def dicee():
    return random.randint(1, 6)

@client.command(aliases=[
    "zaratma"],
    description="To use it  !dc dice")  # Kullanıcının bu komutu kullanmak için illa bu isimi kullanmasına gerek yok.Böylelikle yeni isimler ata-
# yabiliriz.
async def dice( ctx):
    """Selects a number between 1 to 6 randomly."""
    await ctx.send(dicee())

player1 = ""
player2 = ""

turn = ""
gameOver = True

count = 0
board = []
winning_conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]]

@client.command(aliases = ["XOX","noughts and crosses"])
async def start_tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    "Starts tictactoe.You must mention two players."
    global player1
    global player2
    global board
    global gameOver
    global count
    global turn

    if gameOver:
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        gameOver = False
        turn = ""
        count = 0
        if p1.bot or p2.bot:
            await ctx.send("Bot cannot play this game.He is sorry for that :)")

        else:

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine whoe goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            else:

                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")


    else:
        await ctx.send("The game is already in progress.Finish the current one to start a new one")

@client.command()
async def end_tictactoe(ctx):
    """Ends tictactoe"""
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("Stopping current game")
    else:
        await ctx.send("There are no game currently running.")

@client.command(
    description="To use it  !dc place location (the location starts with 1 from top left of the square and increases towards right)")
async def place( ctx, pos: int):  # ctx.author != self.player1/2 ifadesine True diyor.
    """To place X or O to which location you want"""
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    global winning_conditions
    if not gameOver:
        mark = ""
        if ctx.author != turn:
            await ctx.author.send("You cannot place 'x' or 'o' right now.")
            await ctx.message.delete()
            # Burası değişitirebilir.
        elif turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
                await ctx.send(f"It is {player1.mention}'s turn ")
            elif turn == player2:
                mark = ":o2:"
                await ctx.send(f"It is {player2.mention}'s turn")

            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1
                # prints the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                checkWinner(winning_conditions, mark)
                if gameOver:
                    await ctx.send(mark + "wins!")
                elif count >= 9:
                    await ctx.send("It's a tie!")
                    gameOver = True

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1

            else:
                await ctx.send(
                    "Be sure to choose the blank square and be sure to choose a number betw 1 and 9(inclusive)")

        else:
            await ctx.send(f"{ctx.author},It is not your turn")
            await ctx.message.delete()
    else:
        await ctx.send("Please start a new game by using '!dc tictactoe' command")

def checkWinner(winningConditionss, markk):
    global board
    global gameOver
    for condition in winningConditionss:
        if board[condition[0]] == markk and board[condition[1]] == markk and board[
            condition[2]] == markk:
            gameOver = True

@start_tictactoe.error
async def tictactoe_error( ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")








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

"""
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
"""






client.run('ODcyODgyMTAwNTQ4ODIxMDIy.YQwUzg.v0KB8RdiecfMOFK65SiP2C25knc')




# async :  async nın anlamı asenktron demektir.O da kendi kendine,bağımsız çalışan demektir.Buradan da gördüğümüz
# **gibi fonksiyonlar birbirinden bağımsız çalışıyor.Ve herhangi bir çağırılma durumları olmuyorlar.
