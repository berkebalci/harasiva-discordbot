import discord
import urllib3.util
from discord.ext import commands, tasks
from discord.ext.commands import *
import yt_dlp
import os
import asyncio
import aiohttp
import random
import datetime
import textwrap
from urllib3 import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!dc ", intents=intents)

with open("Badwords.txt", "r", encoding="utf-8") as f:
    for c in f:
        badwords = c.split(",")

with open("Roless.txt", "r", encoding="utf-8") as file2:
    liste = file2.read().split(";")
    print(
        liste)  # Bu rollerin falan yazdığı liste. #txt dosyasında aşağı satıra geçildiğinde önceki satırın sonuna \n konur
    # Değişken isimleri ve satır numaraları
    is_new = str(liste[0])
    Oto_mute = str(liste[1])  # 1.eleman
    num_swearwords = int(liste[2])  # 2.eleman
    other_roles = liste[3].split(",")  # 3.
    mod_roles = liste[4].split(",")  # 4.
    owner_roles = liste[5].split(",")  # 5.

ext_file_types = ["jpeg", "jpg", "png", "gif"]
swearword_count = dict()
hata_ayiklama = dict()
swear_time = dict()


@client.event
async def on_ready():
    print("I am ready!")
    await client.change_presence(activity=discord.Game(name="with the code"))


reaction_number1 = 0

@client.event
async def on_message(message):
    global reaction_number1
    if len(message.attachments) > 0 and message.channel.name.startswith("questions"):
        for ext in ext_file_types:
            if message.attachments[0].filename.endswith(ext):
                reaction_number1 = 0
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
        if Oto_mute != "on":
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
                            timee = 0.5  # Bu ifade saati belirtir.
                            if swear_time[str(message.author.id)] >= 1:
                                await mute_person(message, message.author, f"{timee * 2}h", "For too many bad words.")
                            else:
                                await mute_person(message, message.author, f"{timee}h", "For too many bad words.")

                        await message.channel.send("Please do not use that word.")
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
    if (payload.channel_id == 890734899135393814):  # Buradaki id questions 2 adlı channelin id'sidir
        channell = await client.fetch_channel(payload.channel_id)
        messagee = await channell.fetch_message(payload.message_id)  # messagee'in türü Message isimli sınıfa obje.
        for reaction in messagee.reactions:  # checks the reactant isn't a bot and the emoji isn't the one they just reacted with

            if reaction_number1 >= 5 and not payload.member.bot and str(reaction) != str(payload.emoji):
                # removes the reaction
                await messagee.remove_reaction(reaction.emoji, payload.member)
@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)


@client.event
async def on_member_update(before, after):
    global mod_roles
    global other_roles
    if len(before.roles) < len(after.roles):
        # The user has gained a new role, so lets find out which one
        newRole = next(role for role in after.roles if role not in before.roles)
        if newRole.name == "Muted":
            await after.send("Your role has just become 'Muted")

        elif newRole.id == 889933119875055716:
            await after.send("Congratulations!Your role has been upgraded to 'Mod'")
        if not newRole.id in mod_roles:
            if not newRole.name in after.guild.roles:
                other_roles.append(newRole.id)
                if not (newRole.name == "Muted"):
                    await after.send(f"Congratulations!Your role has been upgraded to {newRole.name}")
            # This uses the name but you could always use newRole.id == Roleid here
            # Now, simply put the code you want to run whenever someone gets the "Respected" role here


@client.event
async def on_member_join(member):
    global swearword_count
    swearword_count[str(member.id)] = 0
    hata_ayiklama[str(member.id)] = 0
    swear_time[str(member.id)] = 0
    await member.send("Welcome to the server mate.Nice to see you :D")


@client.event
async def on_member_remove(member):
    global swearword_count
    global swear_time
    swearword_count.pop(str(member.id))
    swear_time.pop(str(member.id))
################   BOT   ##############

@client.command(description="For that command there are a few options"
                            "Playing xxx >>> !dc change_status 1 game_name"
                            "Listening xxx >>> !dc change_status 2 music_name"
                            "Watching xxx >>> !dc change_status 3 video_name")
async def change_status(ctx, activity, *, text):
    """Changes bot's status (Bot)"""
    activities = {
        "1": {"activity": discord.Game(name=text)},
        "2": {"activity": discord.Activity(type=discord.ActivityType.listening, name=text)},
        "3": {"activity": discord.Activity(type=discord.ActivityType.watching, name=text)},
    }
    # Görüldüğü gibi yukarıdaki iki methodta neredeyse aynıdır.Python burada parametrelere bakıyor,hangisinde argüman sayısı fazlaysa onu çalıştırıyor.

    await client.change_presence(**activities.get(activity))  # Böyle yaparak dict objesini unpack ettik.


###############   Bot_Response  ##############
@client.command(aliases=["selamla", "say_hello", "hi"], description="To use the command: !dc greetings")
async def greetings(ctx, *args):  # ctx demek context yani mesajın içeriği anlamına geliyor
    """Bot greets everyone and says its name. (Bot)"""
    print(ctx)  # Bunu yazdırdığımızda <Message id=878026076855623711 channel=<TextChannel id=873962539......
    print(
        ctx.message.channel)  # gibi devam eden bir text beliriyor.Discord bu text içinden mesajın bulunduğu kanalı alıp aşağıdaki
    # kodu çalıştırıyor.
    # Ayrıca bu yapıdan da discord'un bir kişi o channel'a yazı yazdığında o kişinin birçok bilgisine ulaşmamıza yardımcı
    # olduğunu da anlamamız gerekir.
    await ctx.send(f"Hi everyone,my name is {client.user.name}.  I am a Discord Bot :) ")


###############  Fun  ##################################

allowed_animal = ["dog", "cat", "panda", "fox", "red panda", "koala", "bird", "raccoon", "kangaroo"]


@client.command(description= "To use the command: !dc giveaway")
@has_any_role("admin", "Mod")
async def giveaway(ctx):
    """Selects a member in the server except Bot  (Fun)"""
    while True:
        a = random.choice(ctx.guild.members)  # Bu arada bot.guilds ifadesi de bir liste döndürüyor
        if a.bot:
            continue
        else:
            await ctx.send(f"{a},won the giveway,congratulations :)")
            break


@client.command(description="To use the command: !dc animal_fact panda(or some selected animals:\ndog\n"
                            "cat\n"
                            "panda\n"
                            "fox\n"
                            "red panda\n"
                            "koala\n"
                            "bird\n"
                            "raccoon\n"
                            "kangaroo\n"
                            "\n"
                            "Example: !dc animal_fact raccoon")
async def animal_fact(ctx, animal: str):
    """Gives information about specified animal (Fun)"""
    global allowed_animal
    if not (animal in allowed_animal):
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
            dogjson = await request.json()  # dogjson objesi bir dict'dir.
            print(type(request))
            # This time we'll get the fact request as well!
            request2 = await session.get(f'https://some-random-api.ml/facts/{animal}')
            factjson = await request2.json()

        embed = discord.Embed(title="FACT!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


meme_set = set()


@client.command(description="To use the command: !dc meme")
async def meme(ctx):  # print(rjson["id"]) yazınca bir sonuc cıkıyor
    """Sends random meme to the channel (Fun)"""
    global meme_set
    while True:
        async with aiohttp.ClientSession() as r:
            request = await r.get("https://some-random-api.ml/meme")  # Bu API mantığına bakmam gerek.
            rjson = await request.json()

        if (rjson)["id"] in meme_set:
            if len(meme_set) == 12:
                pass

        else:
            meme_set.add(rjson["id"])
            embed = discord.Embed(
                title="Random Meme",
                colour=discord.Colour.orange())

            print(rjson)
            embed.set_image(url=rjson['image'])

            await ctx.send(embed=embed)
            break


############## Music ##################

url_2 = ""
@client.command(description="To use the command: !dc play video_url\n"
                            "Example: !dc play https://www.youtube.com/watch?v=oKUuA1MnCs4")
async def play(ctx, url: str):
    """Plays music  (Music)"""
    global url_2
    global playing_status
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")

    # song_there adlı bir dosya oluşturmalıyız.
    # todo Kullanıcı Bot kanala bağlanmışken bot çıkmadan başka bir şarkı açabilsin.
    # todo Şarkılara bir oynatma listesi yap.

    else:

        url_2 = url
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")




            voiceChannel = ctx.message.author.voice.channel
            await voiceChannel.connect()
            voice = discord.utils.get(client.voice_clients,
                                      guild=ctx.guild)  # Bu bizim botun ses özellikleriyle bağlantımız olacak

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
        except PermissionError:
            await ctx.send("Wait for the current music to stop or use !dc stop to stop music")
        except discord.ClientException:
            print("sj")





@client.command(description= "To use the command: !dc leave\n"
                             "You must use this command if you want to play a song after a song\n"
                             "To play another song>>>First make the bot leave the channel: !dc leave\n"
                             "After that: !dc play https://www.youtube.com/watch?v=oKUuA1MnCs4")
async def leave(ctx):
    """Bot leaves the channel(Music)"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a server.")


@client.command()
async def pause(ctx):
    """Stops current music(Music)"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused ⏸️")
    else:
        await ctx.send("There is no audio playing currently.")


@client.command()
async def resume(ctx):
    """Resumes the current music(Music)"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resuming ▶️")
    else:
        await ctx.send("The audio is already paused")


@client.command()
async def stop(ctx):
    """Stops the current music"""
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("The audio is stopped!")


@client.command(
    aliases=['l', 'lyrc', 'lyric'])  # adding aliases to the command so they they can be triggered with other names
async def lyrics(ctx, *, search):
    """A command to find lyrics easily!"""
    if not search:  # if user hasnt given an argument, throw a error and come out of the command
        embed = discord.Embed(
            title="No search argument!",
            description="You havent entered anything, so i couldnt find lyrics!"
        )
        return await ctx.reply(embed=embed)
        # ctx.reply is available only on discord.py version 1.6.0, if you have a version lower than that use ctx.send
    song = urllib3.util.parse_url(search)  # url-encode the song provided so it can be passed on to the API
    print(song)
    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(
                f'https://some-random-api.ml/lyrics?title={song}') as jsondata:  # define jsondata and fetch from API
            if not 300 > jsondata.status >= 200:  # if an unexpected HTTP status code is recieved from the website, throw an error and come out of the command
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')
            lyricsData = await jsondata.json()  # load the json data into its json form
    error = lyricsData.get('error')
    if error:  # checking if there is an error recieved by the API, and if there is then throwing an error message and returning out of the command
        return await ctx.send(f'Recieved unexpected error: {error}')
    songLyrics = lyricsData['lyrics']  # the lyrics
    songArtist = lyricsData['author']  # the author's name
    songTitle = lyricsData['title']  # the song's title
    songThumbnail = lyricsData['thumbnail']['genius']  # the song's picture/thumbnail
    # sometimes the song's lyrics can be above 4096 characters, and if it is then we will not be able to send it in one single message on Discord due to the character limit
    # this is why we split the song into chunks of 4096 characters and send each part individually
    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace=False):
        embed = discord.Embed(
            title=songTitle,
            description=chunk,
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=songThumbnail)
        await ctx.send(embed=embed)


############  Games  ################

def dicee():
    return random.randint(1, 6)


@client.command(aliases=[
    "zaratma"],
    description="To use it  !dc dice")  # Kullanıcının bu komutu kullanmak için illa bu isimi kullanmasına gerek yok.Böylelikle yeni isimler ata-
# yabiliriz.
async def dice(ctx):
    """Selects a number between 1 to 6 randomly.(Games)"""
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


@client.command(aliases=["XOX", "noughts and crosses"])
async def start_tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    "Starts tictactoe.(Games)"
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
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
                turn = player2
            else:
                turn = player2
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
                turn = player1




    else:
        await ctx.send("The game is already in progress.Finish the current one to start a new one")


@client.command()
async def end_tictactoe(ctx):
    """Ends tictactoe(Games)"""
    if not ((ctx.author.roles in mod_roles) and (ctx.author == player1) or (ctx.author == player2)):
        await ctx.send("You can not stop the current game")
    else:

        global gameOver
        if not gameOver:
            gameOver = True
            await ctx.send("Stopping current game")
        else:
            await ctx.send("There are no game currently running.")


@client.command(
    description="To use it  !dc place location (the location starts with 1 from top left of the square and increases towards right)")
async def place(ctx, pos: int):  # ctx.author != self.player1/2 ifadesine True diyor.
    """Places X or O to given location."""
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
                await ctx.send(f"It is {player2.mention}'s turn ")
            elif turn == player2:
                mark = ":o2:"
                await ctx.send(f"It is {player1.mention}'s turn")

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
        await ctx.send("Please start a new game by using '!dc start_tictactoe' command")


def checkWinner(winningConditionss, markk):
    global board
    global gameOver
    for condition in winningConditionss:
        if board[condition[0]] == markk and board[condition[1]] == markk and board[
            condition[2]] == markk:
            gameOver = True


@start_tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. @player1.")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


############### Social media  #################

class Social:
    TWITTER = "https://twitter.com/"
    INSTAGRAM = "https://instagram.com/"
    YOUTUBE = "https://youtube.com/"
    LINKEDIN = "https://www.linkedin.com/in/"


all_social_medias = {
    "TWITTER": "HaraSivaaa",
    "INSTAGRAM": "harasivaaa",
    "YOUTUBE": "BerkeBalcı",
    "LINKEDIN": "berke-balcı-1b591321b/"}

Room = 0


@client.command(aliases=["sosyal_medya"], description="!dc setSocialmed s abolute_path\n"
                                                      "On above command 's' means which social media you want to set.\n"
                                                      "1 for Twitter\n"
                                                      "2 for INSTAGRAM\n"
                                                      "3 for YOUTUBE\n"
                                                      "4 for LINKEDIN\n"
                                                      "Example: !dc setSocialmed 1 https://twitter.com/HaraSivaaa\n)")
@has_any_role("admin", "Mod")
async def setSocialmed(ctx, s, abolute_path):  # Sosyal medya linklerini değiştirmemizi sağlar.
    """For setting sclmedi links to send to channels."""
    global all_social_medias
    # s değeri hangi socila media hesabını değiştirmek istediğini belirtecek.
    # abolute_path ifadesi sosyal medya linki
    """You can define any social media links(YOUTUBE,LINKEDIN,INSTAGRAM,YOUTUBE)"""
    all_social_medias[s] = abolute_path
    print(all_social_medias)


@client.command(description="To use !dc socialpush #channel_name num(interval) num(count)\n"
                            "Example: !dc socialpush #channel1 2 6\n"
                            "After the above code bot sends your social medias to the specifed channel 2 seconds apart for 6 times.")
async def socialpush(ctx,
                     room: discord.TextChannel, interval=10,
                     count=3):  # Bu sosyal medya linki gönderme olayını başlatan bu fonksiyon.
    """Sends social media links to a channel specified times(Moderation)."""
    global Room
    Room = room
    task = tasks.loop(seconds=interval, count=count)(socialmedia_push)
    task.start()


@client.command()
@has_any_role("admin", "Mod")
async def stop_socialpush(ctx):
    """Stops sending links to the specified channel"""
    socialpush.stop()


async def socialmedia_push(self):
    await Room.send(self.getSocials())


def getSocials(self) -> str:
    return f"""
    {Social.TWITTER}{all_social_medias.get("TWITTER")}
    {Social.YOUTUBE}{all_social_medias.get("YOUTUBE")}
    {Social.INSTAGRAM}{all_social_medias.get("INSTAGRAM")}
    {Social.LINKEDIN}{all_social_medias.get("LINKEDIN")}
"""


#################### Server ###############################
@client.command(description="To use it  !dc ping ")
async def ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    """Shows your ping in the server(Server)"""
    await ctx.send(f"Pong! ({client.latency * 1000}ms)")


@client.command(description="To use it !dc member_info @membername")
@has_any_role(*mod_roles)
async def member_info(ctx, user: discord.Member):
    """Gives information about spesicified member(Server)"""
    mention = []
    for role in user.roles:
        if role.name != "@everyone":
            mention.append(role.mention)

    bb = ", ".join(mention)

    embed = discord.Embed(title="Info:", description=f"Info of: {user.mention}", color=discord.Color.orange())
    embed.add_field(name="Top role:", value=user.top_role)
    embed.add_field(name="Roles:", value=bb)
    embed.add_field(name="Nick Name:", value=str(user.nick))
    embed.add_field(name="Created at:", value=str(user.created_at.strftime("%b %d, %Y")))
    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)


@client.command(description="To use it !dc server_info")
async def server_info(ctx):
    """Gives information about server(Server)"""
    ctxx = ctx.guild
    name = str(ctxx.name)

    description = (ctxx.description)
    owner = ctxx.owner  # Bir member ifadesinin sonuna .mention eklediğimizde @harasiva gibi ifade dönüyor.Bu ifadeye
    # .mention gelicek.

    member_count = str(ctxx.member_count)
    icon = str(ctxx.icon_url)  # URL

    embed = discord.Embed(
        title=name + "  " + "SERVER INFO",
        description=f"Desription: {description}",
        colour=discord.Colour.dark_purple()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Created at:", value=ctx.guild.created_at.strftime("%b %d,%Y"))
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Members", value=member_count, inline=True)
    embed.add_field(name="Premium Subscribers", value=ctxx.premium_subscribers)

    await ctx.send(embed=embed)


@client.command(description="To use it !dc banned list")
async def banned_list(ctx):
    """Sends the list of banned members(Server)"""
    banned_users = await ctx.guild.bans()
    if banned_users == []:
        await ctx.send("There are not any banned users in the server.")
    else:
        for bans in banned_users:
            kullanici1 = bans.user
            await ctx.send(kullanici1.name, kullanici1.discriminator)

    # for x in banned_users diyip x'i yazırdığımızda şu sonuç çıkıyor(servarda banlı 1 kişi var.)
    # BanEntry(reason='Adam 31sjsj dedi abi', user=<User id=805458746394148935 name='Harasivaaa' discriminator='8603' bot=False>


##############  Moderation #######################


@client.command(
    description="It is so important to add roles so that the user can use the command properly.\n"
                "For adding mod roles or more premium roles.!dc add_role mod role_name\n"
                "Example1: !dc add_roles owner m Role2,Role3\n"
                "Example2: !dc add_roles mod s Role1")
async def add_roles(ctx, role_type: str, multiple: str, *, role_name):  # args == role_name
    """Adds roles to memory.(Moderation)"""
    global is_new  # Bu ifadenin bu komutun sonunda falan değiştirilmesi lazım.
    global owner_roles
    global mod_roles
    global other_roles
    guild = ctx.guild
    """new;on;3;&//;!**;|++(Roless.txt'deki ana yapı.)"""
    if is_new == "new":

        sozluk0 = {"mod": "!**", "MOD": "!**", "owner": "|++", "OWNER": "|++", "other": "&//", "OTHER": "&//"}
        belirleyici = sozluk0.get(role_type)
        if not (belirleyici):
            await ctx.send("There are 3 types of roles.mod,owner or other roles.\nPlease use one of them. ")
        else:
            typee = belirleyici

            with open("Roless.txt", "r+", encoding="utf-8") as file:
                content = file.read()
                file.seek(0)
                roles = role_name.split(",")
                if multiple == "m" or multiple == "M":  # For multiple roles

                    # ["NAME","Adam"] >> Bunlar roller
                    if len(roles) <= 1:
                        await ctx.send(
                            "At m(multiple) situation you must enter at least two roles.If you want to add only one role,you should use 's'(singular)\n "
                            "Please add ',' among every two roles you want to add.")
                    else:

                        stringg = ""
                        sayi = 1
                        len_list = len(roles)

                        for x in roles:  # x = "Berke"

                            if not discord.utils.get(guild.roles, name=str(x)):
                                await guild.create_role(name=str(x))
                            if sayi == len_list:  # Bu durum son eleman için
                                stringg += x
                                file.truncate()  # Şu an dosya boş durumda
                                file.seek(0)
                                content = content.replace("new", "no")
                                file.write(content.replace(belirleyici, belirleyici + "," + str(
                                    stringg)))  # txt dosyasına yazdırma işlemi
                                file.seek(0)

                                for c in roles:
                                    if role_type == "mod" or role_type == "Mod":
                                        mod_roles.append(c)  # Programın içindeki değişkenleri değiştirme
                                    elif role_type == "owner" or role_type == "OWNER":
                                        owner_roles.append(c)
                                    elif role_type == "other" or role_type == "OTHER":
                                        other_roles.append(c)

                                is_new = "no"
                                await ctx.send("New roles have been added to bot's background")
                                print(mod_roles)
                                print(other_roles)
                                print(other_roles)

                            else:
                                stringg += x + ","
                                sayi += 1

                # X EKSİK OLABİLİR BAZI KODLARDA ONLARA BAKMALIYIM

                elif multiple == "s" or multiple == "S":
                    # For single role
                    if not (len(roles) <= 1):
                        await ctx.send("If you want to add multiple roles use 'm'.\n"
                                       "Example Usage: !dc add_roles owner m Role1,Role2,Role3")
                    else:

                        if not discord.utils.get(guild.roles, name=str(role_name)):
                            await guild.create_role(name=str(role_name))
                        file.truncate()
                        file.seek(0)
                        content = content.replace("new", "no")
                        file.write(content.replace(belirleyici, belirleyici + "," + role_name))
                        file.seek(0)
                        if role_type == "mod" or role_type == "Mod":
                            mod_roles.append(role_name)  # Programın içindeki değişkenleri değiştirme
                        elif role_type == "owner" or role_type == "OWNER":
                            owner_roles.append(role_name)
                        elif role_type == "other" or role_type == "OTHER":
                            other_roles.append(role_name)

                        await ctx.send("New role has been added to bot's background.")
                        is_new = "no"
                        print(mod_roles)
                        print(other_roles)
                        print(owner_roles)

                else:
                    await ctx.send(
                        "The program couldn't understand if you want to add s(for singular role) or m(for multiple roles).\n"
                        "Example usage: !dc owner m role1,role2,role3")
                    file.write(content)

    elif is_new == "no":

        with open("Roless.txt", "r+", encoding="utf-8") as file:
            content = file.read()
            file.seek(0)
            lines = content.split(";")  # Not defterindeki tek stringi ;'e göre eleman eleman içeren ifade.
            sozluk = {"mod": "!", "MOD": "!", "owner": "|", "OWNER": "|", "other": "&", "OTHER": "&"}  # Ana sözlüğümüz.
            bas_karakter = sozluk.get(role_type)
            if role_type in sozluk.keys():
                roles = role_name.split(",")

                if multiple == "s" or multiple == "S":
                    if not len(roles) == 1:
                        await ctx.send("If you want to add multiple roles use 'm'.\n"  # Kod buraya giriyor
                                       "Example Usage: !dc add_roles owner m Role1,Role2,Role3")
                    else:

                        for x in lines:
                            # Eğer bas_karakter sozlukte varsa ona karsılık gelen ifadeyi dondurecek

                            if bas_karakter:
                                if x.startswith(bas_karakter):
                                    if not discord.utils.get(guild.roles, name=role_name):
                                        await guild.create_role(name=role_name)
                                    file.truncate()
                                    file.seek(0)
                                    file.write(content.replace(x, x + "," + role_name))
                                    file.seek(0)
                                    if role_type == "mod" or role_type == "Mod":
                                        mod_roles.append(role_name)  # Programın içindeki değişkenleri değiştirme
                                    elif role_type == "owner" or role_type == "OWNER":
                                        owner_roles.append(role_name)
                                    elif role_type == "other" or role_type == "OTHER":
                                        other_roles.append(role_name)
                                    await ctx.send("New role has been added to bot's background.")

                                    print(mod_roles)
                                    print(other_roles)
                                    print(owner_roles)


                elif multiple == "m" or multiple == "M":
                    # ["NAME","Adam"] >> Bunlar roller
                    if len(roles) <= 1:
                        await ctx.send(
                            "On m(multiple) situation you must enter at least two roles.If you want to add only one role,you should use 's'(singular)\n "
                            "Please add ',' among every two roles you want to add.")
                    else:
                        for c in lines:
                            if bas_karakter:
                                if c.startswith(bas_karakter):

                                    stringg = ""
                                    sayi2 = 1
                                    len_list = len(roles)

                                    for z in roles:
                                        if not discord.utils.get(guild.roles, name=str(z)):
                                            await guild.create_role(name=str(z))
                                        if sayi2 == len_list:  # Bu durum son eleman için
                                            stringg += z
                                            file.truncate()
                                            file.seek(0)
                                            file.write(content.replace(c, c + "," + stringg))
                                            file.seek(0)
                                            for cc in roles:
                                                if role_type == "mod" or role_type == "Mod":
                                                    mod_roles.append(cc)  # Programın içindeki değişkenleri değiştirme
                                                elif role_type == "owner" or role_type == "OWNER":
                                                    owner_roles.append(cc)
                                                elif role_type == "other" or role_type == "OTHER":
                                                    other_roles.append(cc)
                                            await ctx.send("New roles have been added to bot's background.")
                                            print(mod_roles)
                                            print(other_roles)
                                            print(owner_roles)

                                        else:
                                            stringg += z + ","
                                            sayi2 += 1



                else:

                    await ctx.send(
                        "The program couldn't understand if you want to add s(for singular role) or m(for multiple roles).\n"
                        "Example usage: !dc owner m role1,role2,role3")

            else:
                await ctx.send("Correct usage is:"
                               "!dc add_roles mod(You can change it with owner or other) s(For singular role) role_name")

    else:
        await ctx.send("Something went wrong!")


@add_roles.error
async def add_role_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Input must be like that:!dc add_role mod m role1,role2,role3\n"
                       "NOTE:\n"
                       "In command 'mod' means that the role(s) will define as mod roles.So anyone who has this role would be able to access most of commands")
    if isinstance(error, BadArgument):
        await ctx.send(
            "Input must be like that >> !dc add_role mod m role1,role2,role3\n"
            "!Or >> dc add_role mod s role1")


content_C = ""


@client.command(description= "It is so important to use that command.If you don't,some issues might be occured.\n"
                             "To use the command: !dc remove_roles mod m role_name\n"
                             "Example1: !dc remove_roles owner m Role2,Role3\n"
                             "Example2 !dc remove_roles mod s Role1")
async def remove_roles(ctx, role_type: str, multiple: str, *,
                       role_name):  # Bu methodta rol hem not defterinden hem de serverdan silinir.
    """Removes the given role(s) from memory(Moderation)"""
    global content_C
    global is_new  # Bu ifadenin bu komutun sonunda falan değiştirilmesi lazım.
    global owner_roles
    global mod_roles
    global other_roles
    if is_new == "new":
        await ctx.send("None roles could found.")
    else:

        with open("Roless.txt", "r+", encoding="utf-8") as file:

            guild = ctx.guild
            content = file.read()
            file.seek(0)
            lines = content.split(";")  # Not defterindeki tek stringi ;'e göre eleman eleman içeren ifade.
            sozluk = {"mod": "!**", "MOD": "!**", "owner": "|++", "OWNER": "|++", "other": "&//",
                      "OTHER": "&//"}  # Ana sözlüğümüz.
            bas_karakter = sozluk.get(role_type)

            if role_type in sozluk.keys():
                roles = role_name.split(",")

                if multiple == "s" or multiple == "S":
                    if not len(roles) == 1:
                        await ctx.send("If you want to add multiple roles use 'm'.\n"  # Kod buraya giriyor
                                       "Example Usage: !dc add_roles owner m Role1,Role2,Role3")
                    else:

                        if not ((role_name in other_roles) or (role_name in mod_roles) or (role_name in owner_roles)):
                            await ctx.send("Please be sure that the role you want to remove exists in the server.")
                        else:

                            for x in lines:
                                # Eğer bas_karakter sozlukte varsa ona karsılık gelen ifadeyi dondurecek

                                if bas_karakter == sozluk.get(role_type):
                                    pass
                                    if x.startswith(bas_karakter):

                                        file.truncate()
                                        file.seek(0)
                                        file.write(content.replace(x, x.replace(f",{role_name}", "")))
                                        file.seek(0)
                                        if role_type == "mod" or role_type == "Mod":
                                            mod_roles.remove(role_name)  # Programın içindeki değişkenleri değiştirme
                                        elif role_type == "owner" or role_type == "OWNER":
                                            owner_roles.remove(role_name)
                                        elif role_type == "other" or role_type == "OTHER":
                                            other_roles.remove(role_name)
                                        if discord.utils.get(guild.roles, name=role_name):
                                            role_object = discord.utils.get(ctx.guild.roles, name=role_name)
                                            await role_object.delete()
                                        await ctx.send("New role has been removed from bot's background.")




                elif multiple == "m" or multiple == "M":
                    # ["NAME","Adam"] >> Bunlar roller
                    if len(roles) <= 1:
                        await ctx.send(
                            "On m(multiple) situation you must enter at least two roles.If you want to add only one role,you should use 's'(singular)\n "
                            "Please add ',' among every two roles you want to add.")
                    else:
                        try:

                            kosul_iter = True  # Roles'a yapılan iterasyon işleminin bitip bitemdğini kontrol eder.
                            kosul_ic = False
                            kosul_dis = False

                            for c in lines:
                                if c.startswith(sozluk.get(role_type)):
                                    content_C = str(c)

                                    for c_2 in c:
                                        if kosul_iter:
                                            for z in roles:
                                                if not (discord.utils.get(guild.roles, name=z)):
                                                    await ctx.send(f"The role {z} cannot found in the server.\n"
                                                                   "Please check whether it exist in the server or not.\n ")

                                                    kosul_ic = True

                                                elif not (
                                                        mod_roles.count(z) or other_roles.count(z) or owner_roles.count(
                                                    z)):
                                                    await ctx.send(
                                                        "Please be sure that all the roles you want to remove exist in the server.")
                                                    kosul_ic = True
                                                    break

                                                else:

                                                    content_C = content_C.replace("," + z, "")

                                                    role_object = discord.utils.get(guild.roles, name=z)
                                                    await role_object.delete()
                                                    if role_type == "mod" or role_type == "Mod":
                                                        await ctx.send(
                                                            f"The role {z} has been removed from the server. ")
                                                        mod_roles.remove(
                                                            z)  # Programın içindeki değişkenleri değiştirme
                                                    elif role_type == "owner" or role_type == "OWNER":
                                                        await ctx.send(
                                                            f"The role {z} has been removed from the server. ")
                                                        owner_roles.remove(z)
                                                    elif role_type == "other" or role_type == "OTHER":
                                                        await ctx.send(
                                                            f"The role {z} has been removed from the server. ")
                                                        other_roles.remove(z)

                                            kosul_iter = False
                                            print(mod_roles)
                                            print(other_roles)
                                            print(owner_roles)

                                        if kosul_ic:
                                            kosul_dis = True
                                            break

                                        if c.endswith(c_2) and kosul_iter == False:
                                            print("Bu asamaya girildi.")
                                            print(content_C)
                                            file.truncate()
                                            file.seek(0)
                                            file.write(content.replace(c, content_C))
                                            file.seek(0)
                                            kosul_dis = True

                                            break

                                    if kosul_dis:
                                        break

                        except:
                            await ctx.send("Something went wrong please check your code.\n"
                                           "-Check whether the roles you want to remove exist or not.\n"
                                           "-Check whether you used modes(m or s) or not\n"
                                           "-Check whether you defined the role type(mod or owner or other) or not\n"
                                           "-Check whether you used command right.\n"
                                           "-Check whether you wrote wrong or invalid role names or not.")



                else:

                    await ctx.send(
                        "The program couldn't understand if you want to add s(for singular role) or m(for multiple roles).\n"
                        "Example usage: !dc owner m role1,role2,role3")

            else:
                await ctx.send("Correct usage is:"
                               "!dc add_roles mod(You can change it with owner or other) s(For singular role) role_name")


@remove_roles.error
async def remove_role_error(ctx, error):
    if isinstance(error, AttributeError):
        await ctx.send("Please be sure that your command is similar to:\n"
                       "!dc remove_roles mod m Role1,Role2,Role3")


@client.command(description= "To use the command: !dc show_forbiddenwords ")
async def show_forbiddenwords(ctx):
    """Shows forbidden words in the server(Moderation)"""
    for x in badwords:
        await ctx.send(f"-{x}")
    return


@client.command(description="To use the command: !dc set_forbiddenwords add(or remove) m(multiple) word1,word2...."
                            "Example1: !dc set_forbiddenwords add m Word1,Word2\n"
                             "Example2 !dc set_forbiddenwords remove s Word1")
async def set_forbiddenwords(ctx, tercih, multiple, *, swearwordsss):
    """Removes or Adds forbiddenwords to memory(Moderation)"""
    if not (tercih != "remove" or tercih != "add"):
        await ctx.send("You can remove or add swearwords to the backgorund.\n"
                       "Example Usage:!biddenwords remove m Word1,Word2,Word3,Word4")

    else:

        with open("Badwords.txt", "r+", encoding="utf-8") as file3:
            content = file3.read()
            file3.seek(0)
            swear_words = content.split(",")
            swearwords_input = swearwordsss.split(",")
            if multiple == "s" or multiple == "S":

                if len(swearwords_input) > 1:
                    await ctx.send("At 's' mode you can only add or remove 1 swearword\n"  # Kod buraya giriyor
                                   "Example Usage: !dc forbiddenwords add s Word1 ")
                else:

                    if tercih == "remove":
                        file3.truncate()
                        file3.seek(0)
                        file3.write(content.replace("," + swearwordsss, ""))
                        badwords.remove(swearwordsss)
                        await ctx.send("Forbiddenword has been removed successfully .")

                    elif tercih == "add":
                        file3.truncate()
                        file3.seek(0)
                        file3.write(content.replace(content, content + "," + swearwordsss))
                        badwords.append(swearwordsss)
                        await ctx.send("Forbidden word has been added successfully.")


                    else:
                        await ctx.send("Something went wrong.")
            elif multiple == "m" or multiple == "M":
                if len(swearwords_input) <= 1:
                    await ctx.send("At 'm' mode you can add or remove more than 1 roles to the server\n"
                                   "Example Usage: !dc forbiddenwords add m Word1,Word2,Word3")
                else:
                    if tercih == "add":
                        stringg = ""
                        sayi1 = len(swearwords_input)
                        for x in swear_words:
                            if sayi1 == len(swearwords_input):
                                file3.truncate()
                                file3.seek(0)
                                file3.write(content.replace("," + stringg, ""))
                                for c in swearwords_input:
                                    badwords.append(c)
                                await ctx.send("Forbidden words has been added successfully.")
                            else:
                                stringg += str(x) + ","
                                sayi1 += 1
                    elif tercih == "remove":
                        stringg = ""
                        sayi1 = len(swearwords_input)
                        for x in swear_words:
                            if sayi1 == len(swearwords_input):
                                file3.truncate()
                                file3.seek(0)
                                file3.write(content.replace(content, content + "," + stringg))
                                for c in swearwords_input:
                                    badwords.append(c)
                                await ctx.send("Forbidden words has been added successfully.")
                            else:
                                stringg += str(x) + ","
                                sayi1 += 1
                    else:
                        await ctx.send("You can only remove or add roles.\n"
                                       "Please use 'add' or 'remove' keywords.")
            else:
                await ctx.send("The program couldn't understand what you want to do.\n"
                               "---If you want to add or remove multiple(more than 1) then you need to use 'm'"
                               "Example Usage >>> !dc forbiddenwords remove m Role1,Role2,Role3"
                               "---If you want to add or remove singular (1) role then you need to use 's'"
                               "Example Usage >>> !dc forbiddenwords remove s Role1")


@client.command(description="To use it !dc restart_otomute")
@has_any_role(*mod_roles, *owner_roles)
async def restart_automute(ctx):
    """Restarts the automute(Moderation)"""
    global Oto_mute
    if Oto_mute == "on":
        await ctx.send("Oto mute is working already")
    else:

        with open("Roless.txt", "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)  # Burası değişkenleri değiştrmek için kullandığımız yer.
            f.truncate()
            f.write(content.replace('off', 'on', 1))

        Oto_mute = "on"

        print("Oto_mute has eveluated to on ")
        await ctx.send("Oto mute is active")


@client.command(description="To use !dc stop_otomute")
@has_any_role("admin", "Mod")
async def stop_automute(ctx):
    """Stops the automute(Moderation)"""
    global Oto_mute
    if Oto_mute == "off":
        await ctx.send("Oto mute is stopped already.")
    else:

        with open("Roless.txt", "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            f.write(content.replace("on", "off", 1))
        Oto_mute = "off"
        print("Oto_mute has eveluated to 0")
        await ctx.send("Oto mute is disable")


@client.command(aliases=["clear_messages"], description="To use !dc clear msg_number\n"
                                                        "Example: !dc clear 5\n"
                                                        "After the above command last 5 messages in the channel wiil be deleted.")
@has_any_role("admin", "Mod")
async def clear(ctx, amount: int = 0):  # Bu method ile birlikte de bir kanaldaki mesajları silebileceğiz.
    """Clears messages as many as you describe(Moderation)"""
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f"{amount} messages has been deleted from the channel.")


@clear.error
async def clear_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please fill the required gap in the command.")


@client.command(aliases=["reproduce the channel"], description="To use !dc copy_channel chnl_number\n"
                                                               "Example: !dc copy_channel 5")
@has_any_role("admin", "Mod")
async def copy_channel(ctx, amount=1):
    """Copies channels as many as you describe(Moderation)"""
    for x in range(amount):
        await ctx.channel.clone()


@client.command(description="To use !dc send_timed_msg interval_number count_number your_text channel_id"
                            "Example: !dc send_timed_msg 2 4 Hello mate how are you #general")
@has_any_role("admin", "Mod")
async def send_timed_msg(ctx, *args, channnel: discord.TextChannel):
    """Sends the message and repeats it(Moderation)"""
    interval = int(args[0])
    count = int(args[1])
    text = "".join(args[2:])

    task = tasks.loop(seconds=interval, count=count)(send_timed_messages)
    # decoratorları illa @ ile kullanmamız gerekmez.
    task.start(ctx, text, channnel)


async def send_timed_messages(ctx, text, channel):
    for x in client.get_all_channels():
        if x == channel:
            await x.send(text)


@send_timed_msg.error
async def send_timed_msg_error(ctx):
    await ctx.send("The format of this command must be:\n"
                   "!dc send_timed_msg seconds interval text\n"

                   "---seconds:Time period that you want to send your messages in\n"
                   "---interval:The number of repeating this messages in the specific channel\n"
                   "---text:Your message")


@client.command(aliases=["kick_member"], description="To use !dc kick @membername\n"
                                                     "Example: !dc kick @Harasiva")
@has_any_role("admin", "Mod")
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks specified member(Moderation)"""
    await member.kick(reason=reason)
    await ctx.send(f"{member}'s been kicked from the server")


@client.command(aliases=["ban_member"], description="To use !dc ban @membername\n"
                                                    "Example: !dc ban @Harasiva")
@has_any_role("admin", "Mod")
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans the specified member(Moderation)"""
    dm_channel = await member.create_dm()
    await dm_channel.send(
        "You've been banned from the server.You won't join the server until admin opens your ban.")
    await member.ban(reason=reason)
    await ctx.send(f"{member}'s been banned from the server.")


@client.command(aliases=["unban_member"], description="To use it  !dc unban @member reason(optional)\n"
                                                      "Example: !dc unban @Harasiva For making discord bots ")
@has_any_role("admin", "Mod")
async def unban(ctx, member: discord.Member, *, reason):
    """Unbans the member(Moderation)"""
    # Burada *(asterisk) kullanmamızın sebebi *'dan sonraki her argümanın member objesine
    # gitmesini istememizdir.Çünkü eğer böyle yapmasak ve birinin banını kaldırmak istesek:
    # !dc unban Harasiva Balcı böylece Harasiva ve Balcı ayrı birer parametreler olarak
    # görülecek ve adamın banını açamayacağız.

    banned_users = await ctx.guild.bans()
    for x in banned_users:
        if member.id == x.id:
            await member.unban(reason=reason)
            return
        else:
            await ctx.send("This member is not banned")


@client.command(description="To use it !dc set_numswearwrds number\n"
                            "Example: !dc set_numswearwrds 5   (If someone writes swearwords more than 5 times he/she will get banned.)")
@has_any_role("admin", "Mod")
async def set_numswearwrds(ctx, number):
    """"Changes allowed times of each user's swearwords(Moderation)"""""
    global num_swearwords
    if number == num_swearwords:
        await ctx.send(f"Allowed swear word times is {number} already.")
    else:
        with open("Roless.txt", "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            f.write(content.replace(str(num_swearwords), str(number), 1))  # replace methodu sadece string argüman alır.
        num_swearwords = number
        await ctx.send(f"Allowed swearword time evaluated to {number}.")


# Aşağıdaki kodlar coglar ve sınıflama ile alakalıdır.Amacımız bir python dosyası yüklemek.
@client.command(description="To use it !dc mute @membername time(optional) reason(optional)\n"
                            "Example: !dc mute @Harasiva 5h for trolling\n"
                            "Instead of hours you can use minutes(m) or seconds(s).")
@has_any_role("admin", "Mod")
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time=None, *, reason=None):
    """Mutes the specified user.(Moderation)"""
    if not member:
        await ctx.send("You must mention a member to mute!")
    elif not time:
        await ctx.send("You must mention a time!")
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
                await ctx.send("Invalid duration input")
                return

        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
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
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(seconds)
        await member.remove_roles(mutedRole)
        unmute_embed = discord.Embed(title="Mute over!",
                                     description=f'{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}')
        await ctx.send(embed=unmute_embed)


@client.command(description="To use !dc unmute @membername\n"
                            "Example: !dc unmute @Harasiva")
@has_permissions(manage_messages=True)
@has_any_role("admin", "Mod")
async def unmute(ctx, member: discord.Member):
    """Unmutes a specified user.(Moderation)"""
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",
                          colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)

@client.command(description="To use it  !dc start_voting option1,option2,option3 emoji1 emoji2 emoji3\n"
                            "Example: !dc start_voting Istanbul,New York 😃 😎\n"
                            "After the above command a voting will occur and there will be 2 options.(You can increase number of options and emojis)")
async def start_voting(ctx, choices: str, *emojiss: str):
    """Starts a voting for members(Moderation)"""
    choicess = choices.split(",")
    if len(choicess) != len(emojiss):
        await ctx.send("Please make sure you put ',' between options and number of options and num of emojis are the same")
    else:
        emojis = [*emojiss]
        random_emojis = random.sample(emojis, len(choicess))
        message = await ctx.send(
            f"Please click any emoji which you want to select for voting\n\n {dict(zip(choicess, random_emojis))}")
        # zip fonksiyonu verilen iki iterable'ın her bir elemanını bir tuple içerisinde sunuyor.Yukarırda da mesela (("Berke","😁")) ifadesi bir dict oluyor.
        for emoji in random_emojis:
            await message.add_reaction(emoji)


async def mute_person(ctx, member: discord.Member, time=None, reason=None):
    # ctx = message

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


client.run('ODkzMTc3Mjg0MDQxNzg1MzQ0.YVXqKg.Y46_I2vQO7RfH_mJkEEBTbjpb_s')
