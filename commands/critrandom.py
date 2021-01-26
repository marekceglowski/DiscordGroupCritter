import random
from discord.ext import commands


class CritRandom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="critRandom", help="Returns a random submission from the queue"
    )
    async def get_crit_random(self, ctx):
        # Crit Random
        sub = random.choice(submission_list)
        text = (
            "Random submission to review:\n"
            + "Submission #"
            + str(get_queue_pos(sub.id))
            + "\n"
            + "Link: "
            + sub.jump_url
            + "\n"
            + "*Go to the above link, and reply to the message to give feedback.*\n."
        )
        await dm(ctx.author, text)