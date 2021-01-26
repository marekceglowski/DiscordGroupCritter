import discord
from discord.ext import commands
from services.discord_service import dm

class Check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="check",
        help="Returns your entered items and any responses they have received",
    )
    async def check(self, ctx):
        user_subs = []
        response_str = ""
        for idx, sub in enumerate(submission_list, start=1):
            if ctx.author.id == sub.user.id:
                user_subs.append((sub, idx))
        if len(user_subs) == 0:
            response_str = "You currently have no submissions in the queue!"
        else:
            response_str = (
                    "> .\n**=========================**\n"
                    + "> **Submissions in the group crit queue:**\n"
                    + "> **=========================**\n\n"
            )
            for s_idx, item in enumerate(user_subs, start=1):
                response_str += (
                        "> **[Submission " + str(s_idx) + "]** \n> "
                        + item[0].time.strftime("%Y-%m-%d %H:%M:%S")
                        + " -- Position in queue: "
                        + str(item[1])
                        + "\n"
                        + "> Link: ||<"
                        + item[0].jump_url
                        + ">||\n"
                )
                if item[0].feedback is not None and len(item[0].feedback) > 0:
                    response_str += "> Feedback Recieved: \n"
                    for f_idx, fb in enumerate(item[0].feedback, start=1):
                        response_str += (
                                ">    (" + str(f_idx) + ") ||<" + fb.jump_url + ">||\n"
                        )
                response_str += "\n\n"
        response_str + "\n\n."
        await dm(ctx.author, response_str)