import discord
from discord.ext import commands, tasks
import main
import datetime


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description= "To use it  !dc ping ")
    async def ping(self, ctx):  # Defines a new "context" (ctx) command called "ping."
        """Shows your ping in the server"""
        await ctx.send(f"Pong! ({main.client.latency * 1000}ms)")

    @commands.command(description= "To use it !dc member_info @membername")
    async def member_info(self, ctx, user: discord.Member):
        """Gives information about spesicified member"""
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

    @commands.command(description= "To use it !dc server_info")
    async def server_info(self, ctx):
        """Gives information about server"""
        ctxx = ctx.guild
        name = str(ctxx.name)
        server_banner = str(ctxx.banner_url) #URL
        description = (ctxx.description)
        owner = ctxx.owner  # Bir member ifadesinin sonuna .mention eklediğimizde @harasiva gibi ifade dönüyor.Bu ifadeye
                            #.mention gelicek.
        region = str(ctxx.region)
        member_count = str(ctxx.member_count)
        icon = str(ctxx.icon_url)  #URL

        embed = discord.Embed(
            title= name +"  " +"SERVER INFO",
            description= f"Desription: {description}",
            colour= discord.Colour.dark_purple()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name= "Created at:",value= ctx.guild.created_at.strftime("%b %d,%Y"))
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Members",value= member_count , inline=True)
        embed.add_field(name= "Premium Subscribers",value= ctxx.premium_subscribers)


        await ctx.send(embed= embed)


    @commands.has_any_role(*(main.owner_roles))
    @commands.command(description= "To use it !dc add_modrole roleid.That id can be found if you click to the role.")
    async def add_modrole(ctx, role_id):
        """You can define new mod roles to the bot."""
        main.mod_roles.append(role_id)

    @commands.has_any_role(*(main.owner_roles))
    @commands.command(description= "To use it !dc remove_modrole roleid")
    async def remove_modrole(ctx, role_id):
        """Removes modRole"""
        main.mod_roles.remove(role_id)

    @commands.command(description= "To use it !dc banned list")
    async def banned_list(self, ctx):
        """Sends the list of banned members"""
        banned_users = await ctx.guild.bans()
        if banned_users == []:
            await ctx.send("There are not any banned users in the server.")
        else:
            for bans in banned_users:
                kullanici1 = bans.user
                await ctx.send(kullanici1.name, kullanici1.discriminator)

        # for x in banned_users diyip x'i yazırdığımızda şu sonuç çıkıyor(servarda banlı 1 kişi var.)
        # BanEntry(reason='Adam 31sjsj dedi abi', user=<User id=805458746394148935 name='Harasivaaa' discriminator='8603' bot=False>)


def setup(bot):
    bot.add_cog(Server(bot))
