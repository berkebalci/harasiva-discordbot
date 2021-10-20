import discord
from discord.ext import commands,tasks
import main
import random
import asyncio

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot =bot
    num_swearwords = 3

    @commands.command(description= "To use it !dc restart_otomute")
    @commands.has_any_role("admin", "mekan sahibi=)")
    async def restart_automute(self, ctx):
        """Restarts the otomute"""
        main.Oto_mute = 1
        print("Oto_mute has eveluated to 1")
        await ctx.send("Oto mute is active")

    @commands.has_any_role(*(main.owner_roles))
    @commands.command(description="To use !dc stop_otomute")
    async def stop_automute(self, ctx):
        """Stops the automute"""
        main.Oto_mute = 0
        print("Oto_mute has eveluated to 0")
        await ctx.send("Oto mute is disable")


    @commands.command(aliases=["clear_messages"],description="To use !dc clear msg_number")
    @commands.has_role("admin")  # Bu kodla bu temizleme işlemini sadece admin rolüne sahip kullanıcı yababilecek
    async def clear(self, ctx, amount: int=0):  # Bu method ile birlikte de bir kanaldaki mesajları silebileceğiz.
        """Clears messages as many as you describe"""
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f"{amount} messages has been deleted from the channel.")
#Command raised an exception: TypeError: '>' not supported between instances of 'str' and 'int'

    @clear.error
    async def clear_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please fill the required gap in the command.")

    @commands.command(aliases=["reproduce the channel"],description="To use !dc copy_channel chnl_number")
    async def copy_channel(self, ctx, amount=1):
        """Copies channels as many as you describe"""
        for x in range(amount):
            await ctx.channel.clone()

    @commands.command(description="To use !dc send_timed_msg interval count_number your_text")
    @commands.has_any_role("admin","Mod")
    async def send_timed_msg(self, ctx, *args,chan_id = None):
        """Sends the message and repeat it according to your indicating"""
        interval = int(args[0])
        count = int(args[1])
        text = "".join(args[2:])

        task = tasks.loop(seconds=interval, count=count)(self.send_timed_messages)
        # decoratorları illa @ ile kullanmamız gerekmez.
        task.start(ctx, text, chan_id)

    async def send_timed_messages(self, ctx, text,
                                  chan_id=886984276342620170):  # count ifadesine verdiğimiz sayı kadar fonksiyon çalıştığında,fonksiyon çalışmayı durdurur
        for x in main.client.get_all_channels():
            if x.id == chan_id:
                await x.send(text)

    @send_timed_msg.error
    async def send_timed_msg_error(self, ctx, error):
        await ctx.send("The format of this command must be:\n"
                       "!dc send_timed_msg seconds interval text\n"

                       "---seconds:Time period that you want to send your messages in\n"
                       "---interval:The number of repeating this messages in the specific channel\n"
                       "---text:Your message")

    @commands.command(aliases=["kick_member"],description="To use !dc kick @membername")
    @commands.has_role("admin")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks specified member"""
        await member.kick(reason=reason)
        await ctx.send(f"{member}'s been kicked from the server")

    @commands.command(aliases=["ban_member"],description="To use !dc ban @membername")
    @commands.has_role("admin")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans the specified member"""
        dm_channel = await member.create_dm()
        await dm_channel.send(
            "You've been banned from the server.You won't join the server until admin opens your ban.")
        await member.ban(reason=reason)
        await ctx.send(f"{member}'s been banned from the server.")



    @commands.command(aliases=["unban_member"],description= "To use it  !dc unban membername#xxxx")
    @commands.has_role("admin")
    async def unban(self, ctx, *, member):
        """Unbans the member"""
        # Burada *(asterisk) kullanmamızın sebebi *'dan sonraki her argümanın member objesine
        # gitmesini istememizdir.Çünkü eğer böyle yapmasak ve birinin banını kaldırmak istesek:
        # !dc unban Harasiva Balcı böylece Harasiva ve Balcı ayrı birer parametreler olarak
        # görülecek ve adamın banını açamayacağız.

        banned_users = await ctx.guild.bans()  # Bu ifade banlanmış kulanıcıların bir listesini döndürecek.
        member_name, member_discriminator = member.split(
            "#")  # Kullancıyı unban için kullanıcının adının yanında yazan discriminatora da'ihtiyaç var.
        # Harasiva#5689 mesela.
        for bans in banned_users:
            kullanici = bans.user

            if (kullanici.name, kullanici.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(kullanici)
                await ctx.send(f"{kullanici.name} is no longer banned member.")
                return
            else:
                print("The proper command must be like that: !dc unban Harasiva#4569")

    @commands.command(description= "To use it !dc change_numswearwords")
    async def change_numswearwords(self,ctx, number):
        """"Changes allowed times to swearwords before member gets muted"""""
        main.num_swearwords = number

    # Aşağıdaki kodlar coglar ve sınıflama ile alakalıdır.Amacımız bir python dosyası yüklemek.
    @commands.command(description="To use it !dc mute @membername time(optional) reason(optional)")
    @commands.has_role("admin")
    @commands.has_permissions(manage_messages=True)
    async def mute(self,ctx, member: discord.Member, time = None, *, reason = None):
        """Mutes the specified user."""
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


    @commands.command(description="To use !dc unmute @membername")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("admin")
    async def unmute(self, ctx, member: discord.Member):
        "Unmutes a specified user."
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f" you have unmutedd from: - {ctx.guild.name}")
        embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",
                              colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

    @commands.command(description="To use !dc add_reaction emoji(such as 😏) ")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("admin")
    async def add_reaction(self, ctx, emoji=0):
      """Adds reaction to the message that you've sent"""
      await ctx.message.add_reaction(emoji=emoji)
    @commands.command(description= "To use it  !dc vote value1,value2,value3......")
    async def vote(self,ctx,choices : str,*emojiss : str):
        """Starts a voting for members"""
        choicess = choices.split(",")
        if len(choicess) != len(emojiss):
            await ctx.send("The number of emojis must be same as the number of choices")
        else:
            emojis = [*emojiss]
            random_emojis = random.sample(emojis,len(choicess))
            message = await ctx.send(f"Please click any emoji which you want to select for voting\n\n {dict(zip(choicess,random_emojis))}")
            #zip fonksiyonu verilen iki iterable'ın her bir elemanını bir tuple içerisinde sunuyor.Yukarırda da mesela (("Berke","😁")) ifadesi bir dict oluyor.
            for emoji in random_emojis:
                await message.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Moderation(bot))
