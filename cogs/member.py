import random
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord
import utils.date_util as date_util

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="add",
        help="Add a submission to the queue (eg. \"!add submission text here\")",
    )
    async def add_crit(self, ctx, *, arg):
        submission = _db.add_submission(ctx.message)
        position = _db.get_submission_position_in_queue(submission.message_id)

        await _discord.dm(
            ctx.author,
            "Submission added! Current position in queue: "
            + str(position)
            + "\n"
            + "Link: ||<"
            + ctx.message.jump_url
            + ">||\n",
        )

    @commands.command(
        name="count",
        help="Displays the number of submissions in the queue"
    )
    async def count_crits(self, ctx):

        subs_queue = _db.get_ordered_queue_submissions()

        if subs_queue is None:
            queue_count = 0

        else:
            queue_count = len(subs_queue)

        await ctx.send("Number of items in the queue is " + str(queue_count) + ".")

    @commands.command(
        name="critRandom", help="Returns a random submission from the queue"
    )
    async def get_crit_random(self, ctx):
        # Crit Random
        submission_list = _db.get_ordered_queue_submissions()
        submissions_with_positions = _db.get_submission_positions_in_queue_multi(submission_list)

        sub_pos = random.choice(submissions_with_positions)
        text = (
                "Random submission to review:\n"
                + "Submission #"
                + str(sub_pos[1])
                + "\n"
                + "Link: "
                + sub_pos[0].jump_url
                + "\n"
                + "*Go to the above link, and reply to the message to give feedback.*\n."
        )
        await _discord.dm(ctx.author, text)

    @commands.command(
        name="submissions",
        help="Returns your entered submissions and any feedback they have received",
    )
    async def submissions(self, ctx):
        response_str = ""

        user = _db.get_user_by_author_id(ctx.author.id)
        user_subs_with_info = _db.get_submissions_with_info_by_user_id(user.user_id)

        if user_subs_with_info is None or len(user_subs_with_info) == 0:
            response_str = "You currently have no submissions!"
        else:
            response_str = (
                    ".\n> **==============**\n"
                    + "> **Your Submissions:**\n"
                    + "> **==============**\n\n"
            )
            for s_idx, item in enumerate(user_subs_with_info, start=1):
                user_sub = item.submission
                sub_feedbacks = item.feedbacks
                sub_queue_pos = item.queue_pos

                response_str += (
                        "> **[Submission " + str(s_idx) + "]** \n> "
                        + user_sub.created_at
                        + " -- Position in queue: " + str(sub_queue_pos) + "\n"
                        + "> Link: ||<"
                        + user_sub.jump_url
                        + ">||\n"
                )
                if sub_feedbacks is not None and len(sub_feedbacks) > 0:
                    response_str += "> Feedback Received: \n"
                    for f_idx, fb in enumerate(sub_feedbacks, start=1):
                        response_str += (
                                ">    (" + str(f_idx) + ") ||<" + fb.jump_url + ">||\n"
                        )
                response_str += "\n\n"
        response_str + "\n\n."
        await _discord.dm(ctx.author, response_str)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.reference is not None:
            _db.add_feedback(message)


def setup(bot):
    bot.add_cog(Member(bot))
