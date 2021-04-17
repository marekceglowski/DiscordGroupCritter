import discord
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="next", help="Return next submission from queue")
    async def next(self, ctx):

        authorperms = ctx.author.permissions_in(ctx.channel)
        if not authorperms.manage_messages:
            await ctx.author.send("You don't have the permissions to do that here!")
            return
        submission_list = _db.get_ordered_queue_submissions()

        if submission_list is None:
            await ctx.author.send("You have reviewed all available submissions.")
            return

        _db.set_submission_complete(submission_list[0])

        sub_id = submission_list[0].user_id
        sub_author = self.bot.get_user(sub_id)

        link_text = "Link: " + submission_list[0].jump_url + "\n"

        await sub_author.send(
            "Your submission is currently being reviewed.\n" + link_text
        )

        await ctx.author.send("Submission to review:\n" + link_text)

        if len(submission_list) > 1:
            next_id = submission_list[1].user_id
            next_author = self.bot.get_user(next_id)
            link_text = "Link: " + submission_list[1].jump_url + "\n"
            
            await next_author.send(
                "Your submission is next in the queue.\n" + link_text
            )


def setup(bot):
    bot.add_cog(Admin(bot))
