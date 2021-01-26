import discord
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord

class Add(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="add",
        help="Add a submission to the queue (eg. \"!add submission text here\")",
    )
    async def add_crit(self, ctx, *, arg):
        pos = _db.add_submission(ctx.message)
        await _discord.dm(
            ctx.author,
            "Submission added! Current position in queue: "
            + str(pos)
            + "\n"
            + "Link: ||<"
            + ctx.message.jump_url
            + ">||\n",
        )
