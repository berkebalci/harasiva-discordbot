import discord
from discord.ext import commands
import aiohttp
import random

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    allowed_animal = ["dog", "cat", "panda", "fox", "red panda", "koala", "bird", "raccoon", "kangaroo"]
    @commands.command()
    async def giveaway(self, ctx):
        while True:
            a = random.choice(self.bot.guilds[0].members)  # Bu arada bot.guilds ifadesi de bir liste döndürüyor
            if a.id == 872882100548821022:
                continue
            else:
                await ctx.send(f"{a},won the giveway,congratulations :)")

    @commands.command()
    async def animal_fact(self,ctx,animal : str):
        if not(animal in self.allowed_animal):
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


    @commands.command()
    async def meme(self,ctx):
        """Sends random meme to the channel"""
        async with aiohttp.ClientSession() as r:
            request = await r.get("https://some-random-api.ml/meme")
            rjson = await request.json()

        embed = discord.Embed(
            title= "Random Meme",
            colour= discord.Colour.orange())

        print(rjson)
        embed.set_image(url=rjson['image'])


        await ctx.send(embed= embed)



def setup(bot):
    bot.add_cog(Fun(bot))
