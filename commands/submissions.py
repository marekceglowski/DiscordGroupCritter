import discord
from discord.ext import commands
from services.discord_service import dm
import services.db_service as _db


class Submissions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="submissions",
        help="Returns your entered submissions and any feedback they have received",
    )
    async def submissions(self, ctx):
        response_str = ""

        user = _db.get_user_by_author_id(ctx.author.id)
        user_subs_with_info = _db.get_submissions_with_info_by_user_id(user.id)

        if user_subs_with_info is None or len(user_subs_with_info) == 0:
            response_str = "You currently have no submissions!"
        else:
            response_str = (
                    "> .\n**===============**\n"
                    + "> **Your Submissions:**\n"
                    + "> **===============**\n\n"
            )
            for s_idx, item in enumerate(user_subs_with_info, start=1):
                user_sub = user_subs_with_info.submission
                sub_feedbacks = user_subs_with_info.feedbacks
                sub_queue_pos = user_subs_with_info.queue_pos

                response_str += (
                        "> **[Submission " + str(s_idx) + "]** \n> "
                        + user_sub.created_at.strftime("%Y-%m-%d %H:%M:%S")
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
        await dm(ctx.author, response_str)
