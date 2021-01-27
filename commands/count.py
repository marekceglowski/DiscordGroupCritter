from discord.ext import commands
from services.db_service import db as _db

class Count(commands.Cog):
    def __init__(self, lmy_bot):
        self.bot = lmy_bot

    @commands.command(
        name="count", help="Displays the number of submissions in the queue"
    )
    async def count_crits(self, ctx):

        await ctx.send(
            "Number of items in the queue is " + str(_db.submissions.count({"status" : "pending"})) + "."
        )
