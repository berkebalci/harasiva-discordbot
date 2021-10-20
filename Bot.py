import discord
from discord.ext import commands
import main
class Bot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.command(description= "For that command there are a few options"
                                "Playing xxx >>> !dc change_status game_name"
                                "Listening xxx >>> !dc change_status music_name"
                                "Watching xxx >>> !dc change_status name"
                                "Streaming >>> !dc change_status name url" )
    async def change_status(self, ctx, activity, *, text):
        """Changes bot's status"""
        self.bind_text(text)
        await self.bot.change_presence(**self.activities.get(activity))  # Böyle yaparak dict objesini unpack ettik.

    @commands.command(description= "For that command there are a few options"
                                "Playing xxx >>> !dc change_status game_name"
                                "Listening xxx >>> !dc change_status music_name"
                                "Watching xxx >>> !dc change_status name"
                                "Streaming >>> !dc change_status name url")
    async def change_status(self, ctx, activity, url, *, text):
        """Changes bot's status"""
        # Görüldüğü gibi yukarıdaki iki methodta neredeyse aynıdır.Python burada parametrelere bakıyor,hangisinde argüman sayısı fazlaysa onu çalıştırıyor.
        self.bind_text(text, url)
        await self.bot.change_presence(**self.activities.get(activity))  # Böyle yaparak dict objesini unpack ettik.

    def bind_text(self, text, url=""):
        self.activities = {
            "1": {"activity": discord.Game(name=text)},
            "2": {"activity": discord.Activity(type=discord.ActivityType.listening, name=text)},
            "3": {"activity": discord.Activity(type=discord.ActivityType.watching, name=text)},
            "4": {"activity": discord.Streaming(name=text, url=url)},
        }


def setup(bot):
    bot.add_cog(Bot(bot))
