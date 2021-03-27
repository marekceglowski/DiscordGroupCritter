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

    @commands.command(name="info", help="Returns feedback on current critique")
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        current_submission = _db.get_submission_latest_complete()

        if current_submission is None:
            ctx.author.send("No submission available")
            return

        submission_user = self.bot.get_user(current_submission.user_id)
        if submission_user is None:
            submission_author = "Anon"
        else:
            submission_author = submission_user.display_name

        message_text = (
            "Currently reviewing a submission by {}.\n".format(submission_author)
            + "Link: "
            + current_submission.jump_url
            + "\n"
        )

        feedbacks = _db.get_feedbacks_on_submission(current_submission.message_id)

        if feedbacks is not None:
            feedback_text = "The submission has the following feedback:\n"
            for feedback in feedbacks:
                for idx, feedback in enumerate(feedbacks):
                    feedback_text += (
                        "> " + str(idx + 1) + ". ||<" + feedback.jump_url + ">||\n\n"
                    )
            message_text += feedback_text

        await ctx.author.send(message_text)


def setup(bot):
    bot.add_cog(Admin(bot))
