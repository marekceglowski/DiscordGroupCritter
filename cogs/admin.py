import discord
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="next", help="Return next submission from queue")
    @commands.has_permissions(administrator=True)
    async def next(self, ctx):

        submission_list = _db.get_ordered_queue_submissions()

        if submission_list is None:
            await ctx.author.send("You have reviewed all avialable submissions")
            return

        _db.set_submission_complete(submission_list[0])

        text = "Submission to Review:\n" + "Link: " + submission_list[0].jump_url + "\n"
        await ctx.author.send(text)


def setup(bot):
    bot.add_cog(Admin(bot))
