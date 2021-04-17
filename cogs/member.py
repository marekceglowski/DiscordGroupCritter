import random
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord
import utils.date_util as date_util
import utils.split_util as split_util

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="add",
        help="Add a submission to the queue (eg. \"!add submission text here\")",
    )
    async def add_crit(self, ctx, *, arg):
        if not _discord.is_group_crit_channel(ctx):
            await ctx.author.send("Must add using the group-crit channel.")
            return

        if not arg:
            await ctx.author.send("Must include message with your submission.")
            return

        if arg.lower().startswith('no-live-crit'):
            submission = _db.add_submission(ctx.message, 'skip')
            await ctx.author.send('Submission added! It will not be part of the livestream.')
        else:
            submission = _db.add_submission(ctx.message)
            position = _db.get_submission_position_in_queue(submission.message_id)

            await ctx.author.send(
                "Submission added! Current position in queue: "
                + str(position)
                + "\n"
                + "Link: ||<"
                + ctx.message.jump_url
                + ">||\n",
                embed=None
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

        await ctx.author.send("Number of items in the queue is " + str(queue_count) + ".")
        await ctx.message.delete()

    @commands.command(
        name="crit", help="Returns the next or a random submission from the queue"
    )
    async def get_crit(self, ctx, arg="next"):
        arg = arg.lower()
        
        valid_args = ["next", "random"]

        if arg not in valid_args:
            await ctx.author.send("Invalid input please see `!help` for usage")
            return

        user = _db.get_user_by_author_id(ctx.author.id)
        submission_list = _db.get_ordered_queue_submissions(
            not_user_id=user.user_id, check_user_feedback_id=user.user_id
        )

        if submission_list is None:
            await ctx.author.send("You have reviewed all avialable submissions")
            return

        submissions_with_positions = _db.get_submission_positions_in_queue_multi(
            submission_list
        )

        if arg == "next":
            review_text = "Submission to Review:\n"
            sub_pos = submissions_with_positions[0]

        elif arg == "random":
            review_text = "Random submission to review:\n"
            sub_pos = random.choice(submissions_with_positions)
            
        text = (
            review_text
                + "Submission #"
                + str(sub_pos[1])
                + "\n"
                + "Link: "
                + sub_pos[0].jump_url
                + "\n"
                + "*Go to the above link, and reply to the message to give feedback.*\n."
        )
        await ctx.author.send(text, embed=None)
        await ctx.message.delete()

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
        await ctx.author.send(response_str, embed=None)
        await ctx.message.delete()

    @commands.command(
        name="feedback",
        help="Returns your entered submissions and any feedback they have received",
    )
    async def feedback(self, ctx, arg='none'):

        if arg != 'given' and arg != 'received' and arg != 'both':
            response_str = "Use command `!feedback given`, `!feedback received`, or `!feedback both`"
            await ctx.author.send(response_str, embed=None)

        if arg == 'given' or arg == 'both':
            response_str = "**> ============\n> Feedback Given:\n> ============**\n\n"
            feedbacks = _db.get_feedbacks_given(ctx.author.id)
            for idx, feedback in enumerate(feedbacks):
                response_str += '> ' + str(idx+1) + '. ||<' + feedback.jump_url + '>||\n\n'
            await ctx.author.send(response_str, embed=None)

        if arg == 'received' or arg == 'both':
            await self.submissions(ctx)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
    @commands.command(
        name="clear",
        help="Clears messages from GroupCritter in the DM Channel",
    )
    async def clear(self, ctx, arg='none'):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            async for message in ctx.channel.history(limit=200):
                if message.author == self.bot.user:
                    await message.delete()

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
    @commands.command(
        name="help",
        help="Help"
    )
    async def help(self, ctx):
        response_str = """
Commands:

- `!add <text>` - adds a new submission to the group crit queue
- `!add no-live-crit <text>` - adds a new submission with status 'skip' so it's not in the livestream queue
- `!count` - counts the number of submissions currently in the queue
- `!crit random` - sends you a random submission from the queue to critique (always returns a submission you haven't reviewed)
- `!crit next` - sends you the next submission from the the queue to critique (doesn't shift the queue position, useful if you want to do them in order)
- `!feedback [given|received|both]` - displays feedback you have given, received, or both
- `!stats` - displays your level and how much feedback you have given
- `!submissions` - displays your crit submissions and feedback received

Admin Commands:

- `!next` - moves the queue up one spot and displays a link to the submission
- `!info` - shows a list of all feedback given to the current queue submission        
"""
        await ctx.author.send(response_str, embed=None)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.reference is not None:
            _db.add_feedback(message)

def setup(bot):
    bot.add_cog(Member(bot))
