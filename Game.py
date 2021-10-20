import random

import discord
from discord.ext import commands


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def dicee(self):
        return random.randint(1, 6)

    @commands.command(aliases=[
        "zaratma"],
        description="To use it  !dc dice")  # Kullanıcının bu komutu kullanmak için illa bu isimi kullanmasına gerek yok.Böylelikle yeni isimler ata-
    # yabiliriz.
    async def dice(self, ctx):
        """Selects a number between 1 to 6 randomly."""
        await ctx.send(self.dicee())

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

    @commands.command()
    async def start_tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        "Starts tictactoe.You must mention two players."
        if self.gameOver:
            self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            self.gameOver = False
            self.turn = ""
            self.count = 0

            self.player1 = p1
            self.player2 = p2

            # print the board
            line = ""
            for x in range(len(self.board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + self.board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + self.board[x]

            # determine whoe goes first
            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.player1
                await ctx.send("It is <@" + str(self.player1.id) + ">'s turn.")
            else:

                self.turn = self.player2
                await ctx.send("It is <@" + str(self.player2.id) + ">'s turn.")


        else:
            await ctx.send("The game is already in progress.Finish the current one to start a new one")

    @commands.command()
    async def end_tictactoe(self, ctx):
        """Ends tictactoe"""
        if not self.gameOver:
            self.gameOver = True
            await ctx.send("Stopping current game")
        else:
            await ctx.send("There are no game currently running.")

    @commands.command(
        description="To use it  !dc place location (the location starts with 1 from top left of the square and increases towards right)")
    async def place(self, ctx, pos: int):  # ctx.author != self.player1/2 ifadesine True diyor.
        """To place X or O to which location you want"""
        if not self.gameOver:
            mark = ""
            if ctx.author != self.turn:
                await ctx.author.send("You cannot place 'x' or 'o' right now.")
                await ctx.message.delete()
                # Burası değişitirebilir.
            elif self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":regional_indicator_x:"
                    await ctx.send("It is <@" + str(self.player2.id) + ">'s turn.")
                elif self.turn == self.player2:
                    mark = ":o2:"
                    await ctx.send("It is <@" + str(self.player1.id) + ">'s turn.")

                if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
                    self.board[pos - 1] = mark
                    self.count += 1
                    # prints the board
                    line = ""
                    for x in range(len(self.board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + self.board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + self.board[x]
                    self.checkWinner(self.winning_conditions, mark)
                    if self.gameOver:
                        await ctx.send(mark + "wins!")
                    elif self.count >= 9:
                        await ctx.send("It's a tie!")
                        self.gameOver = True

                    # switch turns
                    if self.turn == self.player1:
                        self.turn = self.player2
                    elif self.turn == self.player2:
                        self.turn = self.player1

                else:
                    await ctx.send(
                        "Be sure to choose the blank square and be sure to choose a number betw 1 and 9(inclusive)")

            else:
                await ctx.send(f"{ctx.author},It is not your turn")
                await ctx.message.delete()
        else:
            await ctx.send("Please start a new game by using '!dc tictactoe' command")

    def checkWinner(self, winningConditionss, markk):
        for condition in winningConditionss:
            if self.board[condition[0]] == markk and self.board[condition[1]] == markk and self.board[
                condition[2]] == markk:
                self.gameOver = True

    @start_tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")


def setup(bot):
    bot.add_cog(games(bot))
