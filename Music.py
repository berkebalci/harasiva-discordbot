import discord
from discord.ext import commands
import os
import main
import youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")

#song_there adlı bir dosya oluşturmalıyız.
        else:
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")


            except PermissionError:
                await ctx.send("Wait for the current music to stop or use !dc stop to stop music")

            voiceChannel = ctx.message.author.voice.channel
            await voiceChannel.connect()
            voice = discord.utils.get(main.client.voice_clients, guild = ctx.guild) # Bu bizim botun ses özellikleriyle bağlantımız olacak

            ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"))


    @commands.command()
    async def leave(self,ctx):
        voice = discord.utils.get(main.client.voice_clients, guild = ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a server.")

    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(main.client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("Paused ⏸️")
        else:
            await ctx.send("There is no audio playing currently.")
    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(main.client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("Resuming ▶️")
        else:
            await ctx.send("The audio is already paused")
    @commands.command()
    async def stop(self,ctx):
        voice = discord.utils.get(main.client.voice_clients, guild = ctx.guild)
        voice.stop()
        await ctx.send("The audio is stopped!")
def setup(bot):
    bot.add_cog(Music(bot))
