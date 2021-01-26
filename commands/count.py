import discord
from discord.ext import commands


class Count(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="count", help="Displays the number of submissions in the queue"
    )
    async def count_crits(self, ctx):
        await ctx.send(
            "Number of items in the queue is " + str(len(submission_list)) + "."
        )