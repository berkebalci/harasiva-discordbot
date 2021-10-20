import discord
from discord.ext import commands,tasks
import main


class Social:
    TWITTER = "https://twitter.com/"
    INSTAGRAM = "https://instagram.com/"
    YOUTUBE = "https://youtube.com/"
    LINKEDIN = "https://www.linkedin.com/in/"


class Social_media(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    all_social_medias = {
        "TWITTER": "HaraSivaaa",
        "INSTAGRAM": "harasivaaa",
        "YOUTUBE": "BerkeBalcı",
        "LINKEDIN": "berke-balcı-1b591321b/"}

    Room = 0

    @commands.command(aliases=["sosyal_medya"],description= "To use !dc setSocialmed ")
    async def setSocialmed(self,ctx, s, abolute_path):  # Sosyal medya linklerini değiştirmemizi sağlar.
        # s değeri hangi socila media hesabını değiştirmek istediğini belirtecek.
        # abolute_path ifadesi sosyal medya linki
        """You can define any social media links(YOUTUBE,LINKEDIN,INSTAGRAM,YOUTUBE)"""
        self.all_social_medias[s] = abolute_path
        print(self.all_social_medias)

    @commands.command(description= "To use !dc socialpush #channel_name num(interval) num(count)")
    async def socialpush(self,ctx,
                         room: discord.TextChannel,interval =10, count = 3):  # Bu sosyal medya linki gönderme olayını başlatan bu fonksiyon.
        """Sends social media links to the specified channel for specified times in specified time"""
        self.Room = room
        task = tasks.loop(seconds= interval,count= count)(self.socialmedia_push)
        task.start()



    @commands.command()
    async def stop_socialpush(self,ctx):
        """Stops sending links to the specified channel"""
        self.socialpush.stop()


    async def socialmedia_push(self):
        await self.Room.send(self.getSocials())

    def getSocials(self) -> str:
        return f"""
        {Social.TWITTER}{self.all_social_medias.get("TWITTER")}
        {Social.YOUTUBE}{self.all_social_medias.get("YOUTUBE")}
    {Social.INSTAGRAM}{self.all_social_medias.get("INSTAGRAM")}
      {Social.LINKEDIN}{self.all_social_medias.get("LINKEDIN")}
    """

def setup(bot):
    bot.add_cog(Social_media(bot))
